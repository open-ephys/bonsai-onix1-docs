# Import necessary packages
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import spikeinterface.extractors as se
from pathlib import Path

#%% Set parameters for loading data

suffix = 0                                                        # Change to match filenames' suffix
data_directory = Path('./')                                       # Change to match files' directory
plot_num_channels = 10                                            # Number of channels to plot
start_t = None                                                    # Plot start time (seconds). "None" starts the plot at the first sample in the recording
end_t = None                                                      # Plot time duration (seconds) "None" ends the plot at the last sample in the recording

# RHD2164 constants
fs_hz = 30e3
gain_to_uV_ephys = 0.195
offset_ephys = 0.195 * -32768
num_channels_ephys = 64
gain_to_uV_aux = 37.4e-6
offset_aux = 0
num_channels_aux = 3

#%%  Load acquisition session data

dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt(data_directory / f'start-time_{suffix}.csv', delimiter=',', dtype=dt, skip_header=1)
print(f'Recording was started at {meta["time"]} GMT')
print(f'Acquisition clock rate was {meta["acq_clk_hz"] / 1e6 } MHz')

#%% Load RHD2164 data

rec_ephys = se.read_binary(data_directory / f'rhd2164-ephys_{suffix}.raw',
                        sampling_frequency=fs_hz,
                        dtype=np.uint16,
                        num_channels=num_channels_ephys,
                        gain_to_uV=gain_to_uV_ephys,
                        offset_to_uV=offset_ephys)
rec_ephys.set_times(np.fromfile(data_directory / f'rhd2164-clock_{suffix}.raw', dtype=np.uint64).astype(np.double) / meta['acq_clk_hz'],
                with_warning=False)
rec_ephys_slice = rec_ephys.time_slice(start_time=start_t, end_time=end_t)

rec_aux = se.read_binary(data_directory / f'rhd2164-aux_{suffix}.raw',
                        sampling_frequency=fs_hz,
                        dtype=np.uint16,
                        num_channels=num_channels_aux,
                        gain_to_uV=gain_to_uV_aux,
                        offset_to_uV=offset_aux)
rec_ephys.set_times(np.fromfile(data_directory / f'rhd2164-clock_{suffix}.raw', dtype=np.uint64).astype(np.double) / meta['acq_clk_hz'],
                with_warning=False)
rec_aux_slice = rec_aux.time_slice(start_time=start_t, end_time=end_t)

#%% Load stimulator data

dt = {'names': ('clock', 'hub_clock', 'origin', 'delay', 'rest_current', 
                'phase_one_current', 'phase_two_current', 'phase_one_duration', 'inter_phase_interval', 'phase_two_duration', 'inter_pulse_interval', 'pulses_per_burst', 'inter_burst_interval', 'bursts_per_train'),
      'formats': ('u8', 'u8', 'B', 'u4', 'f8', 
                  'f8', 'f8', 'u4', 'u4', 'u4', 
                  'u4', 'u4', 'u4', 'u4')}
estim = np.genfromtxt(data_directory / f'estim_{suffix}.csv', delimiter=',', dtype=dt, skip_header=1)

dt = {'names': ('clock', 'hub_clock', 'origin', 'delay', 'channel_one_current', 
                'channel_two_current', 'pulse_duration', 'pulse_period', 'pulses_per_burst', 'inter_burst_interval', 
                'bursts_per_train'),
      'formats': ('u8', 'u8', 'B', 'u4', 'f8', 
                  'f8', 'f8', 'f8', 'u4', 'f8', 
                  'u4')}
ostim = np.genfromtxt(data_directory / f'ostim_{suffix}.csv', delimiter=',', dtype=dt, skip_header=1)

#%% Load BNO055 data

dt = {'names': ('clock', 'euler', 'quat', 'is_quat_id', 'accel', 'grav', 'temp'),
      'formats': ('u8', '(1,3)f8', '(1,4)f8', '?', '(1,3)f8', '(1,3)f8', 'f8')}
bno055 = np.genfromtxt(data_directory / f'bno055_{suffix}.csv', delimiter=',', dtype=dt, skip_header=1)

bno055_time = bno055['clock'] / meta['acq_clk_hz']
bno055_time_mask = np.bitwise_and(bno055_time >= 0 if start_t is None else start_t,
                                  bno055_time <= bno055_time[-1] if end_t is None else end_t)

#%% Load TS4231 data

dt = {'names': ('clock', 'position'),
      'formats': ('u8', '(1,3)f8')}
ts4231 = np.genfromtxt(data_directory / f'calibrated-ts4231_{suffix}.csv', delimiter=',', dtype=dt, skip_header=1)

ts4231_time = ts4231['clock'] / meta['acq_clk_hz']
ts4231_time_mask = np.bitwise_and(ts4231_time >= 0 if start_t is None else start_t,
                                  ts4231_time <= ts4231_time[-1] if end_t is None else end_t)

#%% Plot RHD2164 ephys & stim data

fig, ax = plt.subplots(1, 1)

col_indices = np.arange(plot_num_channels)[np.newaxis, :]
offset_uV = rec_ephys_slice.get_traces(return_scaled=True, channel_ids=np.arange(plot_num_channels)) + 1000 * col_indices
ax.plot(rec_ephys_slice.get_times(), offset_uV)
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Channel Number')
ax.set_yticks(1000 * np.arange(plot_num_channels))
ax.set_yticklabels(np.arange(plot_num_channels))
ax.set_title('RHD2164 Ephys Data')

for stim_clock, stim_origin in zip(estim['clock'], estim['origin']):
    stim_sec = stim_clock / meta['acq_clk_hz']
    line_color = 'k' if stim_origin == 'Register' else 'r'
    ax.axvline(x=stim_sec, color=line_color, alpha=0.25, ls='-')
    
for stim_clock, stim_origin in zip(ostim['clock'], ostim['origin']):
    stim_sec = stim_clock / meta['acq_clk_hz']
    line_color = 'k' if stim_origin == 'Register' else 'r'
    ax.axvline(x=stim_sec, color=line_color, alpha=0.25, ls='--')

ax.legend([Line2D([0], [0], color='k', alpha=0.25, ls='-'),
           Line2D([0], [0], color='k', alpha=0.25, ls='--'),
           Line2D([0], [0], color='r', alpha=0.25, ls='-'),
           Line2D([0], [0], color='r', alpha=0.25, ls='--'),], 
          ['estim (register triggered)', 'ostim (register triggered)', 'estim', 'ostim'], 
          loc='upper right')

scale_bar_length = 1000  # µV
scale_bar_x = ax.get_xlim()[0]
scale_bar_y = ax.get_ylim()[0]

ax.text(scale_bar_x, scale_bar_y,
        f'  {scale_bar_length} µV', 
        va='bottom', ha='left', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.7, edgecolor='none'))
ax.plot([scale_bar_x, scale_bar_x], 
        [scale_bar_y, scale_bar_y + scale_bar_length], 
        'k-', linewidth=2, zorder=10)

fig.set_size_inches((8,8))
fig.tight_layout()

#%% Plot BNO055 and TS4231V1 data

fig, axes = plt.subplots(6, 1, sharex=True)

# Plot RHD2164 aux data
axes[0].plot(rec_aux_slice.get_times(), 
             rec_aux_slice.get_traces(return_scaled=True, channel_ids=np.arange(num_channels_aux)))
axes[0].set_xlabel('Time (seconds)')
axes[0].set_ylabel('Voltage (V)')
axes[0].set_title('RHD2164 Aux Data')

# Plot BNO055 data
axes[1].plot(bno055_time[bno055_time_mask], bno055['euler'].squeeze()[bno055_time_mask])
axes[1].set_xlabel('Time (seconds)')
axes[1].set_ylabel('degrees')
axes[1].set_title('Euler Angles')
axes[1].legend(['Yaw', 'Pitch', 'Roll'],loc='lower right')

axes[2].plot(bno055_time[bno055_time_mask], bno055['quat'].squeeze()[bno055_time_mask])
axes[2].set_xlabel('Time (seconds)')
axes[2].set_title('Quaternions')
axes[2].legend(['X', 'Y', 'Z', 'W'],loc='lower right')

axes[3].plot(bno055_time[bno055_time_mask], bno055['accel'].squeeze()[bno055_time_mask])
axes[3].set_xlabel('Time (seconds)')
axes[3].set_ylabel('m/s\u00b2')
axes[3].set_title('Linear Acceleration')
axes[3].legend(['X', 'Y', 'Z'],loc='lower right')

axes[4].plot(bno055_time[bno055_time_mask], bno055['grav'].squeeze()[bno055_time_mask])
axes[4].set_xlabel('Time (seconds)')
axes[4].set_ylabel('m/s\u00b2')
axes[4].set_title('Gravity Vector')
axes[4].legend(['X', 'Y', 'Z'],loc='lower right')

# Plot TS4231 data
axes[5].plot(ts4231_time[ts4231_time_mask], ts4231['position'].squeeze()[ts4231_time_mask])
axes[5].set_xlabel('Time (seconds)')
axes[5].set_ylabel('Position (units)')
axes[5].set_title('Position Data')
axes[5].legend(['X', 'Y', 'Z'],loc='lower right')

fig.set_size_inches((8,8))
fig.tight_layout()

plt.show()
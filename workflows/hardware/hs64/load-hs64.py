# Import necessary packages
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from pathlib import Path

#%% Set parameters for loading data

suffix = 0                                                        # Change to match filenames' suffix
data_directory = Path('C:/Users/open-ephys/Documents/data/hs64')  # Change to match files' directory
plot_num_channels = 10                                            # Number of channels to plot
start_t = 3.0                                                     # Plot start time (seconds)
dur = 2.0                                                         # Plot time duration (seconds)

# RHD2164 constants
ephys_uV_multiplier = 0.195
aux_uV_multiplier = 37.4
offset = 32768
num_channels = 64

#%%  Load acquisition session data

dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt(data_directory / f'start-time_{suffix}.csv', delimiter=',', dtype=dt, skip_header=1)
print(f'Recording was started at {meta["time"]} GMT')
print(f'Acquisition clock rate was {meta["acq_clk_hz"] / 1e6 } MHz')

#%% Load RHD2164 data

rhd2164 = {}

# Load RHD2164 clock data and convert clock cycles to seconds
rhd2164['time'] = np.fromfile(data_directory / f'rhd2164-clock_{suffix}.raw', dtype=np.uint64) / meta['acq_clk_hz']

# Load and scale RHD2164 ephys data
ephys = np.reshape(np.fromfile(data_directory / f'rhd2164-ephys_{suffix}.raw', dtype=np.uint16), (-1, num_channels))
rhd2164['ephys_uV'] = (ephys.astype(np.float32) - offset) * ephys_uV_multiplier

# Load and scale RHD2164 aux data
aux = np.reshape(np.fromfile(data_directory / f'rhd2164-aux_{suffix}.raw', dtype=np.uint16), (-1, 3))
rhd2164['aux_uV'] = (aux.astype(np.float32) - offset) * aux_uV_multiplier

rhd2164_time_mask = np.bitwise_and(rhd2164['time'] >= start_t, rhd2164['time'] < start_t + dur)

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

# Convert clock cycles to seconds
bno055_time = bno055['clock'] / meta['acq_clk_hz']

bno055_time_mask = np.bitwise_and(bno055_time >= start_t, bno055_time < start_t + dur)

#%% Load TS4231 data

# Load TS4231 data
dt = {'names': ('clock', 'position'),
      'formats': ('u8', '(1,3)f8')}
ts4231 = np.genfromtxt(data_directory / f'calibrated-ts4231_{suffix}.csv', delimiter=',', dtype=dt, skip_header=1)

# Convert clock cycles to seconds
ts4231_time = ts4231['clock'] / meta['acq_clk_hz']

ts4231_time_mask = np.bitwise_and(ts4231_time >= start_t, ts4231_time < start_t + dur)

#%% Plot time series

fig = plt.figure(figsize=(12, 10))

# Plot RHD2164 ephys data
plt.subplot(711)
plt.plot(rhd2164['time'][rhd2164_time_mask], rhd2164['ephys_uV'][:,0:plot_num_channels][rhd2164_time_mask])
plt.xlabel('Time (seconds)')
plt.ylabel('Voltage (µV)')
plt.title('RHD2164 Ephys Data')

# Plot stimulus delivery
ax = plt.gca() 

for stim_clock in estim['clock']:
      stim_sec = stim_clock / meta['acq_clk_hz']
      if stim_sec > start_t and stim_sec < start_t + dur:
            ax.axvline(x=stim_sec, color='k', alpha=0.5, ls='-')
      
for stim_clock in ostim['clock']:
      stim_sec = stim_clock / meta['acq_clk_hz']
      if stim_sec > start_t and stim_sec < start_t + dur:
            ax.axvline(x=stim_sec, color='k', alpha=0.5, ls='--')

ax.legend([Line2D([0], [0], color='k', alpha=0.5, ls='-'),
           Line2D([0], [0], color='k', alpha=0.5, ls='--')], 
          ['estim', 'ostim'])

# Plot RHD2164 aux data
plt.subplot(712)
plt.plot(rhd2164['time'][rhd2164_time_mask], rhd2164['aux_uV'][rhd2164_time_mask])
plt.xlabel('Time (seconds)')
plt.ylabel('Voltage (µV)')
plt.title('RHD2164 Aux Data')

# Plot BNO055 data
plt.subplot(713)
plt.plot(bno055_time[bno055_time_mask], bno055['euler'].squeeze()[bno055_time_mask])
plt.xlabel('Time (seconds)')
plt.ylabel('degrees')
plt.title('Euler Angles')
plt.legend(['Yaw', 'Pitch', 'Roll'])

plt.subplot(714)
plt.plot(bno055_time[bno055_time_mask], bno055['quat'].squeeze()[bno055_time_mask])
plt.xlabel('Time (seconds)')
plt.title('Quaternion')
plt.legend(['X', 'Y', 'Z', 'W'])

plt.subplot(715)
plt.plot(bno055_time[bno055_time_mask], bno055['accel'].squeeze()[bno055_time_mask])
plt.xlabel('Time (seconds)')
plt.ylabel('m/s\u00b2')
plt.title('Linear Acceleration')
plt.legend(['X', 'Y', 'Z'])

plt.subplot(716)
plt.plot(bno055_time[bno055_time_mask], bno055['grav'].squeeze()[bno055_time_mask])
plt.xlabel('Time (seconds)')
plt.ylabel('m/s\u00b2')
plt.title('Gravity Vector')
plt.legend(['X', 'Y', 'Z'])

# Plot TS4231 data
plt.subplot(717)
plt.plot(ts4231_time[ts4231_time_mask], ts4231['position'].squeeze()[ts4231_time_mask])
plt.xlabel('Time (seconds)')
plt.ylabel('Position (units)')
plt.title('Position Data')
plt.legend(['X', 'Y', 'Z'])

fig.tight_layout()

plt.show()
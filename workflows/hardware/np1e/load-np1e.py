# Import necessary packages
import os
import numpy as np
import matplotlib.pyplot as plt
import spikeinterface.extractors as se
import probeinterface
import probeinterface.plotting

#%% Set parameters for loading data

suffix = 0                                                 # Change to match filenames' suffix
data_directory = 'C:/Users/open-ephys/Documents/data/np1e' # Change to match files' directory
plot_num_channels = 10                                     # Number of channels to plot
ap_gain = 1000                                             # Change to the ap band gain used
lfp_gain = 50                                              # Change to the lfp band gain used
start_t = 3.0                                              # Plot start time (seconds)
dur = 2.0                                                  # Plot time duration (seconds)

# If the "Invert Polarity" checkbox was unchecked in the configuration GUI when data was collected,
# set the value below as negative instead of positive
sample_gain = 1171.875

# Neuropixels 1.0 constants
fs_hz_ap = 30e3
fs_hz_lfp = fs_hz_ap / 12
sample_offset = 512
num_channels = 384

#%%  Load acquisition session data

dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt(os.path.join(data_directory, f'start-time_{suffix}.csv'), delimiter=',', dtype=dt, skip_header=1)
print(f'Recording was started at {meta["time"]} GMT')
print(f'Acquisition clock rate was {meta["acq_clk_hz"] / 1e6 } MHz')

#%% Load Neuropixels 1.0 probe data

# Load and scale Neuropixels 1.0 AP data
gain_to_uV_ap = sample_gain / ap_gain
offset_to_uV_ap = -sample_offset * gain_to_uV_ap
rec_ap = se.read_binary(os.path.join(data_directory, f'np1-spike_{suffix}.raw'),
                        sampling_frequency=fs_hz_ap,
                        dtype=np.uint16,
                        num_channels=num_channels,
                        gain_to_uV=gain_to_uV_ap,
                        offset_to_uV=offset_to_uV_ap)
rec_ap.set_times(np.fromfile(os.path.join(data_directory, f'np1-clock_{suffix}.raw'), dtype=np.uint64).astype(np.double) / meta['acq_clk_hz'],
                 with_warning=False)
rec_ap_slice = rec_ap.time_slice(start_time=start_t, end_time=start_t+dur)

# Load and scale Neuropixels 1.0 LFP data
gain_to_uV_lfp = sample_gain / lfp_gain
offset_to_uV_lfp = -sample_offset * gain_to_uV_lfp
rec_lfp = se.read_binary(os.path.join(data_directory, f'np1-lfp_{suffix}.raw'),
                         sampling_frequency=fs_hz_lfp,
                         dtype=np.uint16,
                         num_channels=num_channels,
                         gain_to_uV=gain_to_uV_lfp,
                         offset_to_uV=offset_to_uV_lfp)
rec_lfp.set_times(rec_ap.get_times()[::12], with_warning=False)
rec_lfp_slice = rec_lfp.time_slice(start_time=start_t, end_time=start_t+dur)

#%% Load BNO055 data

dt = {'names': ('clock', 'euler', 'quat', 'is_quat_id', 'accel', 'grav', 'temp'),
      'formats': ('u8', '(1,3)f8', '(1,4)f8', '?', '(1,3)f8', '(1,3)f8', 'f8')}
bno055 = np.genfromtxt(os.path.join(data_directory, f'bno055_{suffix}.csv'), delimiter=',', dtype=dt)

# Convert clock cycles to seconds
bno055_time = bno055['clock'] / meta['acq_clk_hz']

bno055_time_mask = np.bitwise_and(bno055_time >= start_t, bno055_time < start_t + dur)

#%% Plot time series

fig = plt.figure(figsize=(12, 8))

# Plot scaled Neuropixels 1.0 AP data
plt.subplot(611)
plt.plot(rec_ap_slice.get_times(), 
         rec_ap_slice.get_traces(return_scaled=True, channel_ids=np.arange(plot_num_channels)))
plt.xlabel('Time (seconds)')
plt.ylabel('µV')
plt.title('AP Band Voltage')

# Plot scaled Neuropixels 1.0 LFP data
plt.subplot(612)
plt.plot(rec_lfp_slice.get_times(), 
         rec_lfp_slice.get_traces(return_scaled=True, channel_ids=np.arange(plot_num_channels)))
plt.xlabel('Time (seconds)')
plt.ylabel('µV')
plt.title('LFP Band Voltage')

# Plot BNO055 data
plt.subplot(613)
plt.plot(bno055_time[bno055_time_mask], bno055['euler'].squeeze()[bno055_time_mask])
plt.xlabel('Time (seconds)')
plt.ylabel('degrees')
plt.title('Euler Angles')
plt.legend(['Yaw', 'Pitch', 'Roll'])

plt.subplot(614)
plt.plot(bno055_time[bno055_time_mask], bno055['quat'].squeeze()[bno055_time_mask])
plt.xlabel('Time (seconds)')
plt.title('Quaternion')
plt.legend(['X', 'Y', 'Z', 'W'])

plt.subplot(615)
plt.plot(bno055_time[bno055_time_mask], bno055['accel'].squeeze()[bno055_time_mask])
plt.xlabel('Time (seconds)')
plt.ylabel('m/s\u00b2')
plt.title('Linear Acceleration')
plt.legend(['X', 'Y', 'Z'])

plt.subplot(616)
plt.plot(bno055_time[bno055_time_mask], bno055['grav'].squeeze()[bno055_time_mask])
plt.xlabel('Time (seconds)')
plt.ylabel('m/s\u00b2')
plt.title('Gravity Vector')
plt.legend(['X', 'Y', 'Z'])

fig.tight_layout()

#%% Load and plot Neuropixels 1.0 probeinterface probe group

np1_config = probeinterface.io.read_probeinterface(os.path.join(data_directory, f'np1-config.json'))
probeinterface.plotting.plot_probegroup(np1_config, show_channel_on_click=True)

plt.show()
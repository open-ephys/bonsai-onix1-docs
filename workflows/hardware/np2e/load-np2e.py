# Import necessary packages
import os
import numpy as np
import matplotlib.pyplot as plt
import spikeinterface.extractors as se
import probeinterface
import probeinterface.plotting

#%% Set parameters for loading data

suffix = 0                                                 # Change to match filenames' suffix
data_directory = 'C:/Users/open-ephys/Documents/data/np2e' # Change to match files' directory
plot_num_channels = 10                                     # Number of channels to plot
start_t = 3.0                                              # Plot start time (seconds)
dur = 2.0                                                  # Plot time duration (seconds)

# Neuropixels 2.0 constants
fs_hz = 30e3
gain_to_uV = 3.05176
offset_to_uV = -2048 * gain_to_uV
num_channels = 384

#%%  Load acquisition session data

dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt(os.path.join(data_directory, f'start-time_{suffix}.csv'), delimiter=',', dtype=dt, skip_header=1)
print(f'Recording was started at {meta["time"]} GMT')
print(f'Acquisition clock rate was {meta["acq_clk_hz"] / 1e6 } MHz')

#%% Load Neuropixels 2.0 Probe A data

rec_a = se.read_binary(os.path.join(data_directory, f'np2-a-ephys_{suffix}.raw'),
                     sampling_frequency=fs_hz,
                     dtype=np.uint16,
                     num_channels=num_channels,
                     gain_to_uV=gain_to_uV,
                     offset_to_uV=offset_to_uV)
rec_a.set_times(np.fromfile(os.path.join(data_directory, f'np2-a-clock_{suffix}.raw'), dtype=np.uint64).astype(np.double) / meta['acq_clk_hz'],
                with_warning=False)
rec_a_slice = rec_a.time_slice(start_time=start_t, end_time=start_t+dur)

#%% Load Neuropixels 2.0 Probe B data

# rec_b = se.read_binary(os.path.join(data_directory, f'np2-b-ephys_{suffix}.raw'),
#                      sampling_frequency=fs_hz,
#                      dtype=np.uint16,
#                      num_channels=num_channels,
#                      gain_to_uV=gain_to_uV,
#                      offset_to_uV=offset_to_uV)
# rec_b.set_times(np.fromfile(os.path.join(data_directory, f'np2-b-clock_{suffix}.raw'), dtype=np.uint64).astype(np.double) / meta['acq_clk_hz'],
#                 with_warning=False)
# rec_b_slice = rec_b.time_slice(start_time=start_t, end_time=start_t+dur)

#%% Load BNO055 data

dt = {'names': ('clock', 'euler', 'quat', 'is_quat_id', 'accel', 'grav', 'temp'),
      'formats': ('u8', '(1,3)f8', '(1,4)f8', '?', '(1,3)f8', '(1,3)f8', 'f8')}
bno055 = np.genfromtxt(os.path.join(data_directory, f'bno055_{suffix}.csv'), delimiter=',', dtype=dt)

# Convert clock cycles to seconds
bno055_time = bno055['clock'] / meta['acq_clk_hz']

bno055_time_mask = np.bitwise_and(bno055_time >= start_t, bno055_time < start_t + dur)

#%% Plot time series

fig = plt.figure(figsize=(12, 8))

# Plot scaled Neuropixels 2.0 probe A data
plt.subplot(611)
plt.plot(rec_a_slice.get_times(), 
         rec_a_slice.get_traces(return_scaled=True, channel_ids=np.arange(plot_num_channels)))
plt.xlabel('Time (seconds)')
plt.ylabel('µV')
plt.title('Neuropixels 2.0  Probe A')

# Plot scaled Neuropixels 2.0 probe B data
plt.subplot(612)
# plt.plot(rec_b_slice.get_times(), 
#          rec_b_slice.get_traces(return_scaled=True, channel_ids=np.arange(plot_num_channels)))
plt.xlabel('Time (seconds)')
plt.ylabel('µV')
plt.title('Neuropixels 2.0 Probe B')

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

#%% Load and plot Neuropixels 2.0 ProbeInterface probe group

np2_config_a = probeinterface.io.read_probeinterface(os.path.join(data_directory, 'np2-config-a.json'))
# np2_config_b = probeinterface.io.read_probeinterface(os.path.join(data_directory, 'np2-config-b.json'))

fig = plt.figure()

plt.subplot(121)
ax_a = plt.gca()
probeinterface.plotting.plot_probegroup(np2_config_a, show_channel_on_click=True, ax=ax_a)
plt.title('Neuropixels 2.0 Probe A')

plt.subplot(122)
ax_b = plt.gca()
# probeinterface.plotting.plot_probegroup(np2_config_b, show_channel_on_click=True, ax=ax_b)
plt.title('Neuropixels 2.0 Probe B')

plt.show()
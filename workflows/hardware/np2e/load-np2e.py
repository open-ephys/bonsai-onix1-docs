# Import necessary packages
import numpy as np
import matplotlib.pyplot as plt
import spikeinterface.extractors as se
import probeinterface
import probeinterface.plotting

# Parameters
suffix = 0              # Change to match file names' suffix
start_t = 2.0           # When to start plotting ephys data (second)
dur = 5.0               # Duration of ephys data to plot (seconds)
plot_num_channels = 10  # Number of channels to plot

# Constants
fs_hz = 30e3
gain_to_uV = 3.05176
offset_to_uV = -2048 * gain_to_uV
num_channels = 384

# Load acquisition session data
dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt(f'/content/drive/MyDrive/np2e/start-time_{suffix}.csv', delimiter=',', dtype=dt, skip_header=1)
print(f"Recording was started at {meta['time']} GMT")

# Load Neuropixels 2.0 clock data
time = np.fromfile(f'/content/drive/MyDrive/np2e/np2-a-clock_{suffix}.raw', dtype=np.uint64).astype(np.double) / meta['acq_clk_hz']

# Load and scale Neuropixels 2.0 ephys data
rec = se.read_binary(f'/content/drive/MyDrive/np2e/np2-a-ephys_{suffix}.raw',
                     sampling_frequency=fs_hz,
                     dtype=np.uint16,
                     num_channels=num_channels,
                     gain_to_uV=gain_to_uV,
                     offset_to_uV=offset_to_uV)
rec_scaled = rec.get_traces(return_scaled=False, channel_ids=np.arange(plot_num_channels))

# Truncate data based on start_t & dur
b = np.bitwise_and(time >= start_t, time < start_t + dur)
rec_scaled_truncated = rec_scaled[b]
time_truncated = time[b]

# Plot scaled Neuropixels 2.0 ephys data
fig = plt.figure()
fig.suptitle('Neuropixels 2.0 Data')
plt.plot(time_truncated, rec_scaled_truncated)
plt.xlabel("Time (seconds)")
plt.ylabel("Voltage (µV)")

# Load BNO055 data
dt = {'names': ('clock', 'euler', 'quat', 'is_quat_id', 'accel', 'grav', 'temp'),
      'formats': ('u8', '(1,3)f8', '(1,4)f8', '?', '(1,3)f8', '(1,3)f8', 'f8')}
bno055 = np.genfromtxt(f'/content/drive/MyDrive/np2e/bno055_{suffix}.csv', delimiter=',', dtype=dt)

# Load BNO055 clock data
bno055_time = bno055['clock'] / meta['acq_clk_hz']

# Plot BNO055 data
fig = plt.figure()
fig.suptitle('BNO055 Data')
plt.subplot(231)

plt.plot(bno055_time, bno055['euler'].squeeze())
plt.xlabel("Time (seconds)")
plt.ylabel("Angle (degrees)")
plt.legend(['yaw', 'pitch', 'roll'])
plt.title('Euler')

plt.subplot(232)
plt.plot(bno055_time, bno055['quat'].squeeze())
plt.xlabel("Time (seconds)")
plt.legend(['X', 'Y', 'Z', 'W'])
plt.title('Quaternion')

plt.subplot(233)
plt.plot(bno055_time, bno055['accel'].squeeze())
plt.xlabel("Time (seconds)")
plt.ylabel("Acceleration (m/s\u00b2)")
plt.legend(['X', 'Y', 'Z'])
plt.title('Linear Acceleration')

plt.subplot(234)
plt.plot(bno055_time, bno055['grav'].squeeze())
plt.xlabel("Time (seconds)")
plt.ylabel("Acceleration (m/s\u00b2)")
plt.legend(['X', 'Y', 'Z'])
plt.title('Gravity Vector')

plt.subplot(235)
plt.plot(bno055_time, bno055['temp'].squeeze())
plt.xlabel("Time (seconds)")
plt.ylabel("Temperature (°C)")
plt.title('Headstage Temperature')

plt.tight_layout()

# Load and plot Neuropixels 2.0 probeinterface probe group
np2_config = probeinterface.io.read_probeinterface('/content/drive/MyDrive/np2e/np2-config.json')
probeinterface.plotting.plot_probegroup(np2_config, show_channel_on_click=True)

plt.show()# Import necessary packages
import numpy as np
import matplotlib.pyplot as plt
import spikeinterface.extractors as se
import probeinterface
import probeinterface.plotting

# Parameters
suffix = 0                                    # Change to match file names' suffix
start_t = 2.0                                 # When to start plotting ephys data (second)
dur = 5.0                                     # Duration of ephys data to plot (seconds)
plot_num_channels = 10                        # Number of channels to plot
probeinterface_filename = 'np2-config.json'   # Change this to the name of your probeinterface file

# Constants
fs_hz = 30e3
gain_to_uV = 3.05176
offset_to_uV = -2048 * gain_to_uV
num_channels = 384

plt.close('all')

# Load acquisition session data
dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt(f'c:/Users/cshor/Downloads/data/np2-data/start-time_{suffix}.csv', delimiter=',', dtype=dt, skip_header=1)
print(f"Recording was started at {meta['time']} GMT")

# Load Neuropixels 2.0 clock data
time = np.fromfile(f'c:/Users/cshor/Downloads/data/np2-data/np2-a-clock_{suffix}.raw', dtype=np.uint64).astype(np.double) / meta['acq_clk_hz']

# Load and scale Neuropixels 2.0 ephys data
rec = se.read_binary(f'c:/Users/cshor/Downloads/data/np2-data/np2-a-ephys_{suffix}.raw',
                     sampling_frequency=fs_hz,
                     dtype=np.uint16,
                     num_channels=num_channels,
                     gain_to_uV=gain_to_uV,
                     offset_to_uV=offset_to_uV)
rec_scaled = rec.get_traces(return_scaled=False, channel_ids=np.arange(plot_num_channels))

# Truncate data based on start_t & dur
b = np.bitwise_and(time >= start_t, time < start_t + dur)
rec_scaled_truncated = rec_scaled[b]
time_truncated = time[b]

# Plot Neuropixels 2.0 ephys data
fig = plt.figure()
fig.suptitle('Neuropixels 2.0 Data')
plt.plot(time_truncated, rec_scaled_truncated)
plt.xlabel("Time (seconds)")
plt.ylabel("Voltage (µV)")

# Load BNO055 data
dt = {'names': ('clock', 'euler', 'quat', 'is_quat_id', 'accel', 'grav', 'temp'),
      'formats': ('u8', '(1,3)f8', '(1,4)f8', '?', '(1,3)f8', '(1,3)f8', 'f8')}
bno055 = np.genfromtxt(f'c:/Users/cshor/Downloads/data/np2-data/bno055_{suffix}.csv', delimiter=',', dtype=dt)

# Load BNO055 clock data
bno055_time = bno055['clock'] / meta['acq_clk_hz']

# Plot BNO055 data
fig = plt.figure()
fig.suptitle('BNO055 Data')
plt.subplot(231)

plt.plot(bno055_time, bno055['euler'].squeeze())
plt.xlabel("Time (seconds)")
plt.ylabel("Angle (degrees)")
plt.legend(['yaw', 'pitch', 'roll'])
plt.title('Euler')

plt.subplot(232)
plt.plot(bno055_time, bno055['quat'].squeeze())
plt.xlabel("Time (seconds)")
plt.legend(['X', 'Y', 'Z', 'W'])
plt.title('Quaternion')

plt.subplot(233)
plt.plot(bno055_time, bno055['accel'].squeeze())
plt.xlabel("Time (seconds)")
plt.ylabel("Acceleration (m/s\u00b2)")
plt.legend(['X', 'Y', 'Z'])
plt.title('Linear Acceleration')

plt.subplot(234)
plt.plot(bno055_time, bno055['grav'].squeeze())
plt.xlabel("Time (seconds)")
plt.ylabel("Acceleration (m/s\u00b2)")
plt.legend(['X', 'Y', 'Z'])
plt.title('Gravity Vector')

plt.subplot(235)
plt.plot(bno055_time, bno055['temp'].squeeze())
plt.xlabel("Time (seconds)")
plt.ylabel("Temperature (°C)")
plt.title('Headstage Temperature')

plt.tight_layout()

# Load and plot Neuropixels 2.0 probeinterface probe group
np2_config = probeinterface.io.read_probeinterface('c:/Users/cshor/Downloads/data/np2-data/np2-config.json')
probeinterface.plotting.plot_probegroup(np2_config, show_channel_on_click=True)

plt.show()
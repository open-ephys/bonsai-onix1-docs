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
ap_gain = 1000          # Change to the ap band gain used
lfp_gain = 50           # Change to the lfp band gain used

# Constants
fs_hz_ap = 30e3
fs_hz_lfp = fs_hz_ap / 12
sample_offset = 512
sample_gain = 1171.875
num_channels = 384

# Load acquisition session data
dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt(f'/content/drive/MyDrive/np1e/start-time_{suffix}.csv', delimiter=',', dtype=dt, skip_header=1)
print(f"Recording was started at {meta['time']} GMT")

# Load Neuropixels 1.0 AP clock data
ap_time = np.fromfile(f'/content/drive/MyDrive/np1e/np1-clock_{suffix}.raw', dtype=np.uint64).astype(np.double) / meta['acq_clk_hz']

# Load and scale Neuropixels 1.0 AP data
gain_to_uV_ap = sample_gain / ap_gain
offset_to_uV_ap = -sample_offset * gain_to_uV_ap
ap_rec = se.read_binary(f'/content/drive/MyDrive/np1e/np1-spike_{suffix}.raw',
                        sampling_frequency=fs_hz_ap,
                        dtype=np.uint16,
                        num_channels=num_channels,
                        gain_to_uV=gain_to_uV_ap,
                        offset_to_uV=offset_to_uV_ap)
ap_scaled = ap_rec.get_traces(return_scaled=True, channel_ids=np.arange(plot_num_channels))

# Truncate data based on start_t & dur
b = np.bitwise_and(ap_time >= start_t, ap_time < start_t + dur)
ap_scaled_truncated = ap_scaled[b]
ap_time_truncated = ap_time[b]

# Plot scaled Neuropixels 1.0 AP data
fig = plt.figure()
fig.suptitle('Neuropixels 1.0 AP Data')
plt.plot(ap_time_truncated, ap_scaled_truncated)
plt.xlabel("Time (seconds)")
plt.ylabel("Voltage (µV)")

# Load Neuropixels 1.0 LFP clock data
lfp_time = ap_time[::12]

# Load and scale Neuropixels 1.0 LFP data
gain_to_uV_lfp = sample_gain / lfp_gain
offset_to_uV_lfp = -sample_offset * gain_to_uV_lfp
lfp_rec = se.read_binary(f'/content/drive/MyDrive/np1e/np1-lfp_{suffix}.raw',
                         sampling_frequency=fs_hz_lfp,
                         dtype=np.uint16,
                         num_channels=num_channels,
                         gain_to_uV=gain_to_uV_lfp,
                         offset_to_uV=offset_to_uV_lfp)
lfp_scaled = lfp_rec.get_traces(return_scaled=True, channel_ids=np.arange(plot_num_channels))

# Truncate data based on start_t & dur
b = np.bitwise_and(lfp_time >= start_t, lfp_time < start_t + dur)
lfp_scaled_truncated = lfp_scaled[b]
lfp_time_truncated = lfp_time[b]

# Plot scaled Neuropixels 1.0 LFP data
fig = plt.figure()
fig.suptitle('Neuropixels 1.0 LFP Data')
plt.plot(lfp_time_truncated, lfp_scaled_truncated)
plt.xlabel("Time (seconds)")
plt.ylabel("Voltage (µV)")

# Load BNO055 data
dt = {'names': ('clock', 'euler', 'quat', 'is_quat_id', 'accel', 'grav', 'temp'),
      'formats': ('u8', '(1,3)f8', '(1,4)f8', '?', '(1,3)f8', '(1,3)f8', 'f8')}
bno055 = np.genfromtxt(f'/content/drive/MyDrive/np1e/bno055_{suffix}.csv', delimiter=',', dtype=dt)

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

# Load and plot Neuropixels 1.0 probeinterface probe group
np1_config = probeinterface.io.read_probeinterface('/content/drive/MyDrive/np1e/np1-config.json')
probeinterface.plotting.plot_probegroup(np1_config, show_channel_on_click=True)

plt.show()
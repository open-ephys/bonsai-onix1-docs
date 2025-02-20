# Import necessary packages
import numpy as np
import matplotlib.pyplot as plt

# Parameters
suffix = 0              # Change to match file names' suffix
start_t = 2.0           # When to start plotting ephys data (second)
dur = 5.0               # Duration of ephys data to plot (seconds)
plot_num_channels = 10  # Number of channels to plot

# Constants
fs_hz = 30e3
ephys_uV_multiplier = 0.195
aux_uV_multiplier = 37.4
offset = 32768
num_channels = 64

# Load acqusition session data
dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt(f'c:/Users/cshor/Downloads/data/hs64-data/start-time_{suffix}.csv', delimiter=',', dtype=dt, skip_header=1)
print(f"Recording was started at {meta['time']} GMT")

# Load RHD2164 clock data
time = np.fromfile(f'c:/Users/cshor/Downloads/data/hs64-data/rhd2164-clock_{suffix}.raw', dtype=np.uint64) / meta['acq_clk_hz']

# Load RHD2164 ephys data
ephys = np.reshape(np.fromfile(f'c:/Users/cshor/Downloads/data/hs64-data/rhd2164-ephys_{suffix}.raw', dtype=np.uint16), (-1, num_channels))

# Truncate data based on start_t & dur
b = np.bitwise_and(time >= start_t, time < start_t + dur)
ephys_truncated = ephys[b,:].astype(np.double)
time_truncated = time[b]

# Scale truncated RHD2164 ephys data
ephys_scaled_truncated = (ephys_truncated - offset) * ephys_uV_multiplier

# Plot RHD2164 ephys data
fig = plt.figure()
fig.suptitle("RHD2164 Ephys Data")
plt.plot(time_truncated, ephys_scaled_truncated[:,0:plot_num_channels])
plt.xlabel("Time (seconds)")
plt.ylabel("Voltage (µV)")
plt.tight_layout()

# Load RHD2164 aux data
aux = np.reshape(np.fromfile(f'c:/Users/cshor/Downloads/data/hs64-data/rhd2164-aux_{suffix}.raw', dtype=np.uint16), (-1, 3))

# Truncate RHD2164 aux data
aux_truncated = aux[b, :].astype(np.double)

# Scale truncated RHD2164 aux data
aux_truncated_scaled = (aux_truncated - offset) * aux_uV_multiplier

# Plot RHD2164 aux data
fig = plt.figure()
fig.suptitle("RHD2164 Aux Data")
plt.plot(time_truncated, aux_truncated_scaled)
plt.xlabel("Time (seconds)")
plt.ylabel("Voltage (µV)")
plt.tight_layout()

# Load BNO055 data
dt = {'names': ('clock', 'euler', 'quat', 'is_quat_id', 'accel', 'grav', 'temp'),
      'formats': ('u8', '(1,3)f8', '(1,4)f8', '?', '(1,3)f8', '(1,3)f8', 'f8')}
bno055 = np.genfromtxt(f'c:/Users/cshor/Downloads/data/hs64-data/bno055_{suffix}.csv', delimiter=',', dtype=dt)

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

plt.show()
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
ac_uV_multiplier = 0.195
ac_offset = 32768
dc_uV_multiplier = -19.23
dc_offset = 512
num_channels = 32

# Load acqusition session data
dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt(f'c:/Users/cshor/Downloads/data/rhs2116-data/start-time_{suffix}.csv', delimiter=',', dtype=dt, skip_header=1)
print(f"Recording was started at {meta['time']} GMT")

# Load RHS2116 clock data
time = np.fromfile(f'c:/Users/cshor/Downloads/data/rhs2116-data/rhs2116-clock_{suffix}.raw', dtype=np.uint64) / meta['acq_clk_hz']

# Load RHS2116 ac data
ac = np.reshape(np.fromfile(f'c:/Users/cshor/Downloads/data/rhs2116-data/rhs2116-ac_{suffix}.raw', dtype=np.uint16), (-1, num_channels))

# Truncate data based on start_t & dur
b = np.bitwise_and(time >= start_t, time < start_t + dur)
ac_truncated = ac[b,:].astype(np.double)
time_truncated = time[b]

# Scale truncated RHS2116 ac data
ac_truncated_scaled = (ac_truncated - ac_offset) * ac_uV_multiplier

# Plot RHS2116 ac data
fig = plt.figure()
fig.suptitle("RHS2116 AC Data")
plt.plot(time_truncated, ac_truncated_scaled[:,0:plot_num_channels])
plt.xlabel("Time (seconds)")
plt.ylabel("Voltage (µV)")
plt.tight_layout()

# Load RHS2116 dc data
dc = np.reshape(np.fromfile(f'c:/Users/cshor/Downloads/data/rhs2116-data/rhs2116-dc_{suffix}.raw', dtype=np.uint16), (-1, num_channels))

# Truncate RHS2116 dc data
dc_truncated = dc[b,:].astype(np.double)

# Scale truncated RHD2164 dc data
dc_truncated_scaled = (dc_truncated - dc_offset) * dc_uV_multiplier

# Plot RHS2116 dc data
fig = plt.figure()
fig.suptitle("RHS2116 DC Data")
plt.plot(time_truncated, dc_truncated_scaled[:,0:plot_num_channels])
plt.xlabel("Time (seconds)")
plt.ylabel("Voltage (µV)")
plt.tight_layout()

plt.show()
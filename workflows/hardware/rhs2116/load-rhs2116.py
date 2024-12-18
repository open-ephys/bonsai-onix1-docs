import os
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

#%% Set Parameters for Loading Data

suffix = '0'; # Change to match file names' suffix
# Change this to the directory of your data. In this example, data's in the same directory as this data loading Python script
data_directory = os.path.dirname(os.path.realpath(__file__))
start_t = 1.0 # when to start plotting data (seconds)
dur = 1.0 # duration of data to plot

#%% Metadata

dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt(os.path.join(data_directory, f'start-time_{suffix}.csv'), delimiter=',', dtype=dt)
print(f"Recording was started at {meta['time']} GMT")

#%% RHS2116 ephys data

start_t = 1.0 # when to start plotting data (seconds)
dur = 1.0 # duration of data to plot

rhs2116 = {}
rhs2116['time'] = np.fromfile(os.path.join(data_directory, f'rhs2116-clock_{suffix}.raw'), dtype=np.uint64) / meta['acq_clk_hz']
b = np.bitwise_and(rhs2116['time'] >= start_t, rhs2116['time'] < start_t + dur)
time = rhs2116['time'][b]

# AC data
rhs2116['ac'] = np.reshape(np.fromfile(os.path.join(data_directory, f'rhs2116-ac_{suffix}.raw'), dtype=np.uint16), (-1, 32))
rhs2116_ac = rhs2116['ac'][b, :].astype(np.double)
bit_depth = 16
scalar = 0.195
offset = (2 ** (bit_depth - 1)) * scalar
rhs2116_ac_converted = rhs2116_ac * scalar - offset + np.arange(rhs2116_ac.shape[1])[None, :] * offset / 4

# DC data
rhs2116['dc'] = np.reshape(np.fromfile(os.path.join(data_directory, f'rhs2116-dc_{suffix}.raw'), dtype=np.uint16), (-1, 32))
rhs2116_dc = rhs2116['dc'][b, :].astype(np.double)
bit_depth = 10
scalar = -19.23
offset = (2 ** (bit_depth - 1)) * -scalar
rhs2116_dc_converted = rhs2116_dc * scalar - offset + np.arange(rhs2116_dc.shape[1])[None, :] * offset / 4

def setup_subplot(ax):
      ax.set_yticks([])
      ax.set_ylabel("channel")
      ax.set_xlabel("time (s)")

fig, (ax_ac, ax_dc) = plt.subplots(nrows=1, ncols=2, figsize=(10,8))
ax_ac.plot(time, rhs2116_ac_converted, 'k', linewidth=0.25)
ax_ac.set_title('RHS2116 AC Data')
setup_subplot(ax_ac)
ax_dc.plot(time, rhs2116_dc_converted, 'k', linewidth=0.25)
ax_dc.set_title('RHS2116 DC Data')
setup_subplot(ax_dc)
fig.suptitle('RHS2116 Data')
plt.tight_layout()
plt.show()
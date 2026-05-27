# Import necessary packages
import os
import numpy as np
import matplotlib.pyplot as plt

#%% Set parameters for loading data

suffix = 0                                                    # Change to match filenames' suffix
data_directory = 'C:/Users/open-ephys/Documents/data/rhs2116' # Change to match files' directory
plot_num_channels = 10                                        # Number of channels to plot
start_t = 3.0                                                 # Plot start time (seconds)
dur = 2.0                                                     # Plot time duration (seconds)

# RHS2116 constants
ac_uV_multiplier = 0.195
ac_offset = 32768
dc_mV_multiplier = -19.23
dc_offset = 512
num_channels = 32 # for two RHS2116 devices per headstage

#%%  Load acquisition session data

dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt(os.path.join(data_directory, f'start-time_{suffix}.csv'), delimiter=',', dtype=dt, skip_header=1)
print(f"Recording was started at {meta['time']} GMT")
print(f'Acquisition clock rate was {meta["acq_clk_hz"] / 1e6 } MHz')

#%% Load RHS2116 data

rhs2116 = {}

# Load RHS2116 clock data and convert clock cycles to seconds
rhs2116['time'] = np.fromfile(os.path.join(data_directory, f'rhs2116-clock_{suffix}.raw'), dtype=np.uint64) / meta['acq_clk_hz']

# Load and scale RHS2116 AC data
ac = np.reshape(np.fromfile(os.path.join(data_directory, f'rhs2116-ac_{suffix}.raw'), dtype=np.uint16), (-1, num_channels))
rhs2116['ac_uV'] = (ac.astype(np.float32) - ac_offset) * ac_uV_multiplier

# Load and scale RHS2116 DC data
dc = np.reshape(np.fromfile(os.path.join(data_directory, f'rhs2116-dc_{suffix}.raw'), dtype=np.uint16), (-1, num_channels))
rhs2116['dc_mV'] = (dc.astype(np.float32) - dc_offset) * dc_mV_multiplier

rhs2116_time_mask = np.bitwise_and(rhs2116['time'] >= start_t, rhs2116['time'] < start_t + dur)

#%% Plot time series

fig = plt.figure(figsize=(12, 6))

# Plot RHS2116 AC data
plt.subplot(211)
plt.plot(rhs2116['time'][rhs2116_time_mask], rhs2116['ac_uV'][:,0:plot_num_channels][rhs2116_time_mask])
plt.xlabel('Time (seconds)')
plt.ylabel('Voltage (µV)')
plt.title('RHS2116 AC Data')

# Plot RHS2116 DC data
plt.subplot(212)
plt.plot(rhs2116['time'][rhs2116_time_mask], rhs2116['dc_mV'][:,0:plot_num_channels][rhs2116_time_mask])
plt.xlabel('Time (seconds)')
plt.ylabel('Voltage (mV)')
plt.title('RHS2116 DC Data')

plt.tight_layout()

plt.show()
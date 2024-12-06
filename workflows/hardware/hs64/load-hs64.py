import os
import numpy as np
import matplotlib.pyplot as plt

# Load data from headstage64 tutorial workflow
suffix = '0'; # Change to match file names' suffix
# Change this to the directory of your data. In this example, data's in the same directory as this data loading Python script
data_directory = os.path.dirname(os.path.realpath(__file__))
start_t = 1.0 # when to start plotting data (seconds)
dur = 1.0 # duration of data to plot

plt.close('all')

#%% Metadata
dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt(os.path.join(data_directory, f'start-time_{suffix}.csv'), delimiter=',', dtype=dt, skip_header=1)
print(f"Recording was started at {meta['time']} GMT")

#%% RHD2164 ephys data
start_t = 1.0 # when to start plotting data (seconds)
dur = 1.0 # duration of data to plot
plot_channel_offset_uV = 1000 # Vertical offset between each channel in the time series

hs64 = {}
hs64['time'] = np.fromfile(os.path.join(data_directory, f'rhd2164-clock_{suffix}.raw'), dtype=np.uint64) / meta['acq_clk_hz']
hs64['ephys'] = np.reshape(np.fromfile(os.path.join(data_directory, f'rhd2164-ephys_{suffix}.raw'), dtype=np.uint16), (-1, 64))

# Make arrays for plotting
b = np.bitwise_and(hs64['time'] >= start_t, hs64['time'] < start_t + dur)
time = hs64['time'][b]
rhd2164_ephys = hs64['ephys'][b, :].astype(np.double)

# Convert to uV and offset each channel by some plot_channel_offset_uV 
bit_depth = 16
scalar = 0.195
offset = (2 ** (bit_depth - 1)) * scalar
rhd2164_ephys = rhd2164_ephys * scalar - offset + np.arange(rhd2164_ephys.shape[1])[None, :] * offset / 4

fig = plt.figure()
plt.plot(time, rhd2164_ephys, 'k', linewidth=0.25)
plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False) 
plt.xlabel("time (sec)")
plt.ylabel("channel")
plt.title('RHD2164 Ephys Data')
fig.set_size_inches(5,8)
plt.tight_layout()

#%% RHD2164 aux data
hs64['aux'] = np.reshape(np.fromfile(os.path.join(data_directory, f'rhd2164-aux_{suffix}.raw'), dtype=np.uint16), (-1, 3))

# Make arrays for plotting
b = np.bitwise_and(hs64['time'] >= start_t, hs64['time'] < start_t + dur)
time = hs64['time'][b]
rhd2164_aux = hs64['aux'][b, :].astype(np.double)

# Convert to uV and offset each channel by some plot_channel_offset_uV 
scalar = 37.4
rhd2164_aux_wave = (rhd2164_aux - 2 **(bit_depth - 1)) * scalar

plt.figure()
plt.plot(time, rhd2164_aux_wave)
plt.xlabel("time (sec)")
plt.ylabel("channel")
plt.title('RHD2164 Auxiliary Data')

#%% Bno055
dt = {'names': ('clock', 'euler', 'quat', 'is_quat_id', 'accel', 'grav', 'temp'),
      'formats': ('u8', '(1,3)f8', '(1,4)f8', '?', '(1,3)f8', '(1,3)f8', 'f8')}
bno055 = np.genfromtxt(os.path.join(data_directory, f'bno055_{suffix}.csv'), delimiter=',', dtype=dt)

bno055_time = bno055['clock'] / meta['acq_clk_hz']

plt.figure()

plt.subplot(231)
plt.plot(bno055_time, bno055['euler'].squeeze())
plt.xlabel("time (sec)")
plt.ylabel("angle (deg.)")
plt.ylim(-185, 365)
plt.legend(['yaw', 'pitch', 'roll'])
plt.title('Euler')

plt.subplot(232)
plt.plot(bno055_time, bno055['quat'].squeeze())
plt.xlabel("time (sec)")
plt.ylim(-1.1, 1.1)
plt.legend(['X', 'Y', 'Z', 'W'])
plt.title('Quaternion')

plt.subplot(233)
plt.plot(bno055_time, bno055['accel'].squeeze())
plt.xlabel("time (sec)")
plt.ylabel("accel. (m/s^2)")
plt.legend(['X', 'Y', 'Z'])
plt.title('Lin. Accel.')

plt.subplot(234)
plt.plot(bno055_time, bno055['grav'].squeeze())
plt.xlabel("time (sec)")
plt.ylabel("accel. (m/s^2)")
plt.legend(['X', 'Y', 'Z'])
plt.title('Gravity Vec.')

plt.subplot(235)
plt.plot(bno055_time, bno055['temp'].squeeze())
plt.xlabel("time (sec)")
plt.ylabel("temp. (°C)")
plt.title('Headstage Temp.')

plt.tight_layout()

#%% TS4231
dt = {'names': ('clock', 'position'),
      'formats': ('u8', '(1,3)f8')}
ts4231 = np.genfromtxt(os.path.join(data_directory, f'ts4231_{suffix}.csv'), delimiter=',', dtype=dt)

ts4231_time = ts4231['clock'] / meta['acq_clk_hz']
plt.figure()

plt.plot(ts4231_time, ts4231['position'].squeeze())
plt.xlabel("time (sec)")
plt.ylabel("position (units)")
plt.legend(['x', 'y', 'z'])
plt.title('Position Data')

plt.show()
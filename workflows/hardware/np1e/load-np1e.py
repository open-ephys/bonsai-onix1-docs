import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import spikeinterface.extractors as se
import spikeinterface.widgets as sw
import probeinterface
import probeinterface.plotting

ap_gain = 500 # Change to the ap band gain used
lfp_gain = 500 # Change to the lfp band gain used
suffix = 0 # Change to match file names' suffix
num_channels = 384 # Decrease channels to expedite plotting and inspect fewer traces
# Change this to the directory of your data. In this example, data's in the same directory as this data loading Python script
data_directory = os.path.dirname(os.path.realpath(__file__))
mode = 'auto' # This uses colormap plot above 50 channels and line plot below 50 channels. Refer to the spikeinterface docs for more options
# Change this to the name of your probeinterface file (should be in the same directory as the rest of your data for this example script to work as-is)
probeinterface_filename = 'np1-config.json'


plt.close('all')

#%% Metadata
dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt(os.path.join(data_directory, f'start-time_{suffix}.csv'), delimiter=',', dtype=dt, skip_header=1)
print(f"Recording was started at {meta['time']} GMT")

#%% Neuropixels 1.0 probeinterface
fig, ax = plt.subplots()
np1_config = probeinterface.io.read_probeinterface(os.path.join(data_directory,  'np1-config.json'))
contacts_colors = ['cyan' if device_channel_index > -1 else 'red' for device_channel_index in np1_config.probes[0].device_channel_indices]
probeinterface.plotting.plot_probegroup(np1_config, ax=ax, contacts_colors=contacts_colors, contacts_kargs={'alpha' : 1, 'zorder' : 10}, show_channel_on_click=True)
fig.set_size_inches(2, 9)
enabled = mpatches.Patch(color='cyan', label='Enabled')
disabled = mpatches.Patch(color='red', label='Disabled')
fig.legend(handles=[enabled, disabled], loc='outside upper center') 
plt.tight_layout()


#%% Neuropixels 1.0 Data
bit_depth = 10
fig, ax = plt.subplots(1,2)
fig.suptitle('Neuropixels 1.0 Data')
fig.set_size_inches(9, 9)
plt.subplots_adjust(wspace=0.3)

ap_scalar = 1.2e6 / (2 ** bit_depth) / ap_gain
ap_offset = (2 ** (bit_depth - 1)) * ap_scalar
ap_recording = se.read_binary(os.path.join(data_directory,  f"np1-spike_{suffix}.raw"), 
                           3e5, 
                           np.uint16, 
                           num_channels, 
                           gain_to_uV=ap_scalar, 
                           offset_to_uV=-ap_offset) 
ap_traces_plot = sw.plot_traces(ap_recording, 
                   backend='matplotlib', 
                   return_scaled=True, 
                   mode=mode, 
                   clim=(-ap_offset,ap_offset),
                   ax=ax[0])
ax[0].set_xlabel("time (sec)")
ax[0].set_ylabel("AP (µV)")

lfp_scalar = 1.2e6 / (2 ** bit_depth) / lfp_gain
lfp_offset = (2 ** (bit_depth - 1)) * lfp_scalar
lfp_recording = se.read_binary(os.path.join(data_directory,  f"np1-lfp_{suffix}.raw"), 
                           3e5/12, 
                           np.uint16, 
                           num_channels, 
                           gain_to_uV=lfp_scalar, 
                           offset_to_uV=-lfp_offset) 
lfp_traces_plot = sw.plot_traces(lfp_recording, 
                   backend='matplotlib', 
                   return_scaled=True, 
                   mode=mode, 
                   clim=(-lfp_offset,lfp_offset), 
                  ax=ax[1])
ax[1].set_xlabel("time (sec)")
ax[1].set_ylabel("LFP (µV)")

#%% Bno055
dt = {'names': ('clock', 'euler', 'quat', 'is_quat_id', 'accel', 'grav', 'temp'),
      'formats': ('u8', '(1,3)f8', '(1,4)f8', '?', '(1,3)f8', '(1,3)f8', 'f8', '?')}
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

plt.show()

fig.suptitle('BNO055 Data')

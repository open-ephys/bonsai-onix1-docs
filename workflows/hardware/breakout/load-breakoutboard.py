import numpy as np
import matplotlib.pyplot as plt

# Load data from breakout board tutorial workflow
path = '' # Set to the directory of your data from the example workflow
suffix = '0' # Change to match file names' suffix
plt.close('all')

#%% Metadata
dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt(path + '/start-time_' + suffix + '.csv', delimiter=',', dtype=dt)
print(f"Recording was started at {meta['time']} GMT")

#%% Analog Inputs
analog_input = {}
analog_input['time'] = np.fromfile(path + '/analog-clock_' + suffix + '.raw', dtype=np.uint64) / meta['acq_clk_hz']
analog_input['data'] = np.reshape(np.fromfile(path + '/analog-data_' + suffix + '.raw', dtype=np.float32), (-1, 12))

plt.figure()
plt.plot(analog_input['time'], analog_input['data'])
plt.xlabel("time (sec)")
plt.ylabel("volts")
plt.legend(['Ch. 0', 'Ch. 1', 'Ch. 2', 'Ch. 3', 'Ch. 4', 'Ch. 5', 
            'Ch. 6', 'Ch. 7', 'Ch. 8', 'Ch. 9', 'Ch. 10', 'Ch. 11'])

#%% Digital Inputs
digital_input = {}
digital_input['time'] = np.fromfile(path + '/digital-clock_' + suffix + '.raw', dtype=np.uint64) / meta['acq_clk_hz']
digital_input['pins'] = np.fromfile(path + '/digital-pins_' + suffix + '.raw', dtype=np.uint8)
digital_input['buttons'] = np.fromfile(path + '/digital-buttons_' + suffix + '.raw', dtype=np.uint16)

digital_input['pins_b'] = np.unpackbits(digital_input['pins'], bitorder='little').reshape(-1, 8).astype(bool)
digital_input['buttons_b'] = np.unpackbits(digital_input['buttons'].astype(np.uint8), bitorder='little').reshape(-1, 8).astype(bool)

line_spacing = 1.25

# digital pin data
pins = ['Pin 0', 'Pin 1', 'Pin 2', 'Pin 3', 'Pin 4', 'Pin 5', 'Pin 6', 'Pin 7']

plt.figure()
for i in range(len(pins)):
    plt.step(digital_input['time'], digital_input['pins_b'][:,i] + line_spacing * i, color='k')
plt.ylim(-0.5, len(pins) * line_spacing + 0.5)
plt.yticks(np.arange(0.5, len(pins) * line_spacing, line_spacing), pins)
plt.title('Digital I/O Data')
plt.tight_layout()

#digital button data
buttons = ['Moon', 'Triangle', 'X', 'Check', 'Circle', 'Square']

plt.figure()
for i in range(len(buttons)):
    plt.step(digital_input['time'], digital_input['buttons_b'][:,i] + line_spacing * i, color="k")
plt.ylim(-0.5, len(buttons) * line_spacing + 0.5)
plt.yticks(np.arange(0.5, len(buttons) * line_spacing, line_spacing), buttons)
plt.title('Button Data')
plt.tight_layout()

plt.show()

#%% Hardware FIFO buffer use
dt = {'names': ('clock', 'bytes', 'percent'),
      'formats': ('u8', 'u4', 'f8')}
memory_use = np.genfromtxt('memory-use_' + suffix + '.csv', delimiter=',', dtype=dt)

plt.figure()
plt.plot(memory_use['clock'] / meta['acq_clk_hz'], memory_use['percent'])
plt.xlabel("time (sec)")
plt.ylabel("FIFO used (%)")

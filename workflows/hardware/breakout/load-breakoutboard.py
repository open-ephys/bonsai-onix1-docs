import numpy as np
import matplotlib.pyplot as plt

# Load data from breakout board tutorial workflow
suffix = '0'; # Change to match file names' suffix
plt.close('all')

#%% Metadata
dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt('start-time_' + suffix + '.csv', delimiter=',', dtype=dt)
print(f"Recording was started at {meta['time']} GMT")

#%% Analog Inputs
analog_input = {}
analog_input['time'] = np.fromfile('analog-clock_' + suffix + '.raw', dtype=np.uint64) / meta['acq_clk_hz']
analog_input['data'] = np.reshape(np.fromfile('analog-data_' + suffix + '.raw', dtype=np.float32), (-1, 12))

plt.figure()
plt.plot(analog_input['time'], analog_input['data'])
plt.xlabel("time (sec)")
plt.ylabel("volts")
plt.legend(['Ch. 0', 'Ch. 1', 'Ch. 2', 'Ch. 3', 'Ch. 4', 'Ch. 5', 
            'Ch. 6', 'Ch. 7', 'Ch. 8', 'Ch. 9', 'Ch. 10', 'Ch. 11'])

#%% Digital Inputs
digital_input = {}
digital_input['time'] = np.fromfile('digital-clock_' + suffix + '.raw', dtype=np.uint64) / meta['acq_clk_hz']
digital_input['pins'] = np.fromfile('digital-pins_' + suffix + '.raw', dtype=np.uint16)
digital_input['buttons'] = np.fromfile('digital-buttons_' + suffix + '.raw', dtype=np.uint16)

def sort_digital_data(time, digital_data, num_inputs):
    digital_data_sorted = []
    for i in range(0, num_inputs):
        digital_data_sorted.append((time[0], i, (digital_data[0] >> i) & 1))
    state_previous = digital_data[0]
    for clock_current, state_current in zip(time[1:], digital_data[1:]):
        state_delta = state_previous ^ state_current
        for i in range(0, num_inputs):
            if (state_delta >> i) & 1:
                digital_data_sorted.append((clock_current, i, (state_current >> i) & 1))
        state_previous = state_current
    dt = np.dtype([('Clock', np.float64), ('Digital Input', np.uint8), ('State', np.bool_)])
    return np.array(digital_data_sorted, dtype=dt)

num_pins = 8
num_buttons = 12
pins_data = sort_digital_data(digital_input['time'], digital_input['pins'], num_pins)
buttons_data = sort_digital_data(digital_input['time'], digital_input['buttons'], num_buttons)

def plot_digital_data(digital_data, num_digital_inputs, legend_labels, plot_title):
    plt.figure()
    line_spacing = 1.25
    for i in range(0, num_digital_inputs):
        index_mask = digital_data['Digital Input'] == i
        plt.step(digital_data['Clock'][index_mask], digital_data['State'][index_mask] + line_spacing * i, color="black")
    plt.ylim(-0.5, num_digital_inputs * line_spacing + 0.5)
    plt.yticks(np.arange(0.5, num_digital_inputs * line_spacing, line_spacing), legend_labels)
    plt.title(plot_title)
    plt.tight_layout()

buttons_flags = ['Moon', 'Triangle', 'X', 'Check', 'Circle', 'Square', 'Reserved0', 'Reserved1', 'PortDOn', 'PortCOn', 'PortBOn', 'PortAOn']
plot_digital_data(pins_data, num_pins, range(0, num_pins), "Pins")
plot_digital_data(buttons_data, num_buttons, buttons_flags, "Buttons")

plt.show()

#%% Hardware FIFO buffer use
dt = {'names': ('clock', 'bytes', 'percent'),
      'formats': ('u8', 'u4', 'f8')}
memory_use = np.genfromtxt('memory-use_' + suffix + '.csv', delimiter=',', dtype=dt)

plt.figure()
plt.plot(memory_use['clock'] / meta['acq_clk_hz'], memory_use['percent'])
plt.xlabel("time (sec)")
plt.ylabel("FIFO used (%)")

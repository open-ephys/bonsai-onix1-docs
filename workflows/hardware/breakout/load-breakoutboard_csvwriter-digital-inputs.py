import numpy as np
import matplotlib.pyplot as plt
import csv

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
digital_input_flags = ['Pin0', 'Pin1', 'Pin2', 'Pin3', 'Pin4', 'Pin5', 'Pin6', 'Pin7',
                       'Moon', 'Triangle', 'X', 'Check', 'Circle', 'Square',
                       'Reserved0', 'Reserved1', 'PortDOn', 'PortCOn', 'PortBOn', 'PortAOn']
digital_input_data = []
with open("digital-data_" + suffix + '.csv', 'r') as digital_input_file:
      digital_input_reader = csv.reader(digital_input_file)
      row = [entry.strip() for entry in next(digital_input_reader)]
      time = int(row[0]) / meta['acq_clk_hz']
      for digital_input_flag in digital_input_flags:
            if digital_input_flag in [entry.strip() for entry in row[1:]]:
                  digital_input_data.append((time, digital_input_flag, True))
            else:
                  digital_input_data.append((time, digital_input_flag, False))
      row_previous = row
      for row in digital_input_reader:
            time = int(row[0]) / meta['acq_clk_hz']
            row = [entry.strip() for entry in row]
            for entry in (set(row) | set(row_previous)):
                  if (entry in row_previous[1:]) and (not entry in row[1:]):
                        digital_input_data.append((time, entry, False))
                  elif (not entry in row_previous[1:]) and (entry in row[1:]): 
                        digital_input_data.append((time, entry, True))
            row_previous = row

dt = np.dtype([('Clock', np.float64), ('Digital Input', '<U10'), ('State', np.bool_)])
digital_input_data = np.array(digital_input_data, dtype=dt)

plt.figure()
line_spacing = 1.25
for i, digital_input_flag in enumerate(digital_input_flags):
      index_mask = digital_input_data['Digital Input'] == digital_input_flag
      line = plt.step(digital_input_data['Clock'][index_mask], digital_input_data['State'][index_mask] + line_spacing * i, color="black")
plt.ylim(-0.5, len(digital_input_flags) * line_spacing + 0.5)
plt.yticks(np.arange(0.5, len(digital_input_flags) * line_spacing, line_spacing), digital_input_flags)
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

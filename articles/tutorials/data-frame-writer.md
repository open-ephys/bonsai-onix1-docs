---
uid: data-frame-writer
title: Using DataFrameWriter to Save Data
---

The <xref:OpenEphys.Onix1.DataFrameWriter.DataFrameWriter> operator provides an
easy and efficient way to write [ONIX data](xref:data-elements) to disk using
the [Apache Arrow file format](https://arrow.apache.org/docs/format/Intro.html).
Apache Arrow stores data in a column-oriented binary layout where values from
each channel or signal are packed contiguously on disk. Each file also embeds a
schema containing column names, data types, and structure, so no separate
metadata file is needed to read it correctly. This tutorial explains how to use
`DataFrameWriter` in an acquisition workflow, configure its properties
(including optional compression), and efficiently load the resulting Arrow files
in Python.

The first section walks through how to save, load, and plot data written by a
`DataFrameWriter` using Python. More detailed explanation are considered in the
[Advanced](#advanced-arrow-topics) at the end of this article.

> [!NOTE]
> Arrow is supported by many scientific computing environments. For instance:
>
> - [Python](https://arrow.apache.org/docs/python/index.html)
>   - With [NumPy](https://arrow.apache.org/docs/python/numpy.html) integration
>   - With [Pandas](https://arrow.apache.org/docs/python/pandas.html) integration
>   - With [Polars](https://pola.rs/) integration
> - [R](https://arrow.apache.org/docs/r/)
> - [Julia](https://arrow.apache.org/julia/stable/)
> - [Matlab](https://github.com/apache/arrow/blob/main/matlab/README.md)

## Save Arrow data

### Adding DataFrameWriter to a workflow

<xref:OpenEphys.Onix1.DataFrameWriter.DataFrameWriter> is a sink operator that accepts any device
data stream that produces <xref:OpenEphys.Onix1.DataFrame> or
<xref:OpenEphys.Onix1.BufferedDataFrame> elements. In practice, this means it can be placed
downstream of virtually any [data source operator](xref:datasource).

You can use multiple `DataFrameWriter` nodes in the same workflow, placing one per data stream. Give
each node a descriptive `FileName` so recordings are easy to identify after the fact. For more
details on the available properties, see the [properties section](#dataframewriter-properties) below.

::: workflow
![workflow for testing DataFrameWriter with Breakout Board data](../../workflows/tutorials/data-frame-writer/data-frame-writer-example.bonsai)
:::

### DataFrameWriter properties

`DataFrameWriter` exposes the following properties in the Bonsai property panel. The full API
reference is on the <xref:OpenEphys.Onix1.DataFrameWriter.DataFrameWriter> page.

- **FileName** The path of the output file, including the `.arrow` extension (e.g.,
  `data/memory-monitor.arrow`). Any intermediate directories in the path are created automatically
  if they do not already exist.

- **Suffix** A modifier inserted into the file name just before the extension each time the
  workflow starts. Choose one of three options:
  - `None` (default): No suffix is added. If a file at the specified path already exists and
    `Overwrite` is `false`, the workflow raises an error on startup.
  - `FileCount`: Appends an underscore followed by a count of files already in the same directory
    with the same base name and extension (`_0`, `_1`, `_2`, …). Use this to automatically number
    successive recordings without having to rename the node before each run.
  - `Timestamp`: Appends an underscore followed by a high-resolution system timestamp at the moment
    the file is created (ISO 8601 format), guaranteeing a unique file name for every run.

- **Buffered** (default: `true`) When `true`, incoming frames are placed in a memory queue and
  written to disk by a background thread, preventing disk I/O latency from blocking the acquisition
  thread. Setting this to `false` writes synchronously on the acquisition thread, which is not
  recommended for high-bandwidth data streams or when low latency feedback is required.

- **Overwrite** (default: `false`) When `true`, an existing file at the resolved path is
  silently replaced when the workflow starts. When `false`, the workflow raises an error if the file
  already exists. This setting has no practical effect when `Suffix` is `FileCount` or `Timestamp`,
  because those modes always produce a unique file name.

- **EnableCompression** (default: `false`) When `true`, data is compressed with
  [Zstandard](https://facebook.github.io/zstd/) before being written to disk. See the
  [Compression](#compression) section for guidance on when to enable this.

### Compression

Setting `EnableCompression` to `True` instructs `DataFrameWriter` to compress
each record batch using the [Zstandard](https://facebook.github.io/zstd/) codec
before writing it to disk. Zstandard is an open-source general-purpose
compression algorithm that offers a good balance between compression ratio and
speed. For typical neural data, enabling compression can substantially
reduce file sizes.

#### When to enable compression

Enable compression when storage space is a constraint and the additional CPU
load during acquisition is acceptable. Compression runs on the same machine that
is acquiring data, so it competes with the rest of your acquisition pipeline for
CPU resources (although enabling the `Buffered` [property](#dataframewriter-properties) can
alleviate this). For most workloads this overhead is negligible, but for very
high-bandwidth configurations (e.g., multiple Neuropixels probes) or when
running other computationally intensive processing in the same workflow,
benchmark your system before relying on compression in long recordings.

> [!TIP]
> A practical way to evaluate the impact of compression on your specific
> setup is to use a <xref:OpenEphys.Onix1.MemoryMonitorData> operator to
> examine the state of the hardware buffer when `EnableCompression` is set to
> True or False. If the `PercentUsed` value remains near zero in both cases,
> compression is not impacting the real-time performance in your workflow. See
> the [closed-loop performance tutorial](xref:tune-readsize) for more information
> on real-time optimization.

## Load Arrow data

In Python, Arrow files can be read using
[PyArrow](https://arrow.apache.org/docs/python/index.html). Notably, several
scientific analysis libraries such as [pandas](https://pandas.pydata.org/),
[numpy](https://numpy.org/) and [Polars](https://pola.rs/), use PyArrow
internally to support loading Arrow files into their environment. In this
section, we will demonstrate file loading using both PyArrow and Pandas.

### Installation

To follow along with the examples in this section, you will need Python,
PyArrow, and pandas. Once Python is installed, run the following command to
install the required packages:

```
pip install pyarrow pandas
```

### Loading script

Download the following script locally, and place the file in the same directory as other processing
scripts. This script has one public function (`load_arrow_file`) which can be used to load an Arrow
file. The following code snippets indicate how to call the function, and some of the options that
can be leveraged when loading.

[Download loading script](../../scripts/tutorials/data-frame-writer/load_arrow.py)

<details>
<summary>View the loading script inline.</summary>

[!code-python[](../../scripts/tutorials/data-frame-writer/load_arrow.py)]
</details>

### Load Arrow data

To load the full Arrow file, simply call `load_arrow_file` with a string
pointing to the file; this can be an absolute file path or a relative file path.

[!code-python[](../../scripts/tutorials/data-frame-writer/load-file.py)]

The optional `start` and `end` parameters are integers that specify the first
and last row indices (0-based) to read from the file. The optional `columns`
parameter is a list of strings that restricts loading to specific channels by
name. Any combination of these parameters can be used together to avoid loading
the full file into memory, which can reduce load time significantly for large
recordings.

[!code-python[](../../scripts/tutorials/data-frame-writer/load-file-with-optional-parameters.py)]

If `start` or `end` is outside the valid row index range, an `IndexError` is
raised indicating what the valid range is. If any string in `columns` does not
match a column name in the file, a `KeyError` is raised.

> [!NOTE]
> Compressed and uncompressed files are loaded identically. PyArrow reads the
> compression metadata in each record batch header and decompresses
> automatically when necessary. This decompression process can incur CPU overhead
> that extends the amount of time it takes to load a file. 

## Working with subsampled data

Some ONIX device data frames contain data from streams that are acquired at
different rates. For example, <xref:OpenEphys.Onix1.NeuropixelsV1DataFrame>
combines AP-band spike data sampled at 30 kHz and LFP-band data sampled at 2.5
kHz. Therefore one LFP sample corresponds to 12 consecutive primary-rate
(AP-band) samples.

When `DataFrameWriter` writes these frames, all columns in the resulting Arrow
file share the same number of rows, set by the primary (faster) rate. Each
subsampled value occupies `divisor` consecutive rows. For instance, each 2.5 kHz
LFP sample appears in 12 consecutive rows of the file. Calling `.to_numpy()` on
a subsampled column therefore returns an array in which every distinct value is
repeated `divisor` times. To recover only the unique samples you need to take
every `divisor`-th row; the divisor for each device and data type is listed on
the relevant data frame API page.

### Extracting unique subsampled values

The script below uses the known sample rate divisor to build a boolean mask that
selects only the rows containing new data. The same mask is applied to the
`Clock` column so that timestamps remain consistent with the subsampled data.

[!code-python[](../../scripts/tutorials/data-frame-writer/load-subsampled-data.py)]

After applying the mask, `data_unique` and `clock_unique` contain only the distinct LFP samples.
Divide `clock_unique` by the acquisition clock rate to convert clock counts to seconds. See
[Reading the acquisition clock rate](#reading-the-acquisition-clock-rate) for how to load that
value from the metadata CSV file.

### Converting to other formats

PyArrow can convert Arrow tables into several other formats for use with different libraries and
workflows.

#### Converting to a pandas DataFrame

If your analysis uses pandas, you can convert an Arrow Table to a DataFrame by calling `.to_pandas()`:

```python
from load_arrow import load_arrow_file

table = load_arrow_file("memory-monitor_0.arrow")
df = table.to_pandas()
```

> [!IMPORTANT]
> Calling `.to_pandas()`, or any other method that converts the table to a pandas DataFrame, might
> copy the entire dataset into RAM. Pandas and PyArrow can, in certain limited circumstances,
> maintain memory mapping across boundaries, but it is not guaranteed. Keep this in mind when
> working with long recordings on machines with limited memory.

#### Using pandas directly

It is also possible to load an Arrow file directly with Pandas using
[`pandas.read_feather()`](https://pandas.pydata.org/docs/reference/api/pandas.read_feather.html),
which accepts Arrow IPC files directly because [Feather
v2](https://arrow.apache.org/docs/python/feather.html#feather-file-format) and Arrow IPC share the
same binary format.

```python
import pandas as pd

df = pd.read_feather("memory-monitor_0.arrow", dtype_backend="pyarrow")
```

This is convenient for short recordings, but it calls PyArrow internally and
loads the entire file into RAM regardless of how large it is. It also does not
expose sample-index access, so there is no way to read only a portion of the
recording without first loading the whole file. For large or long recordings,
the memory-mapped approach described previously is preferable.

#### Exporting to NumPy

Individual columns can be extracted as NumPy arrays using `.to_numpy()`. For large recordings,
replace `reader.read_all()` with a batch loop using `reader.get_batch(i)` and process each batch
incrementally (as shown [below](#manually-loading-arrow-files)) to avoid loading the entire file
into RAM at once.

```python
from load_arrow import load_arrow_file

table = load_arrow_file("memory-monitor_0.arrow")

percent_used = table["PercentUsed"].to_numpy()
clock = table["Clock"].to_numpy()
```

## Plot Arrow data

The examples in this section also require `matplotlib`. Install it alongside the
packages above if you have not already:

```
pip install matplotlib
```

To render and interact with figures, you will also need a `matplotlib` backend.
See the [matplotlib backend
documentation](https://matplotlib.org/stable/users/explain/figure/backends.html)
for installation instructions.

This section shows how to plot data saved from a `MemoryMonitor` device. The
MemoryMonitor schema contains columns including `Clock`, `PercentUsed`, and
`BytesUsed`. The `Clock` column records the raw acquisition clock count and must
be divided by the acquisition clock rate to produce a time value in seconds.

### Reading the acquisition clock rate

The example workflow shown [above](#adding-dataframewriter-to-a-workflow) writes
acquisition metadata, including the clock rate, to a `start-time_<suffix>.csv`
file each time it runs. Load it with NumPy before plotting:

```python
import numpy as np

dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt("start-time_0.csv", delimiter=',', dtype=dt)
acq_clk_hz = meta['acq_clk_hz']
```

### Plotting directly from a PyArrow table

PyArrow column arrays implement the [Python array
protocol](https://arrow.apache.org/docs/python/numpy.html), so most plotting
libraries, including Matplotlib, can consume them directly without an explicit
conversion step. The `Clock` column is an exception: arithmetic operations such
as dividing by the clock rate require a call to `.to_numpy()` first to produce a
NumPy array.

```python
import pyarrow as pa
import numpy as np
import matplotlib.pyplot as plt
from load_arrow import load_arrow_file

dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt("start-time_0.csv", delimiter=',', dtype=dt)
acq_clk_hz = meta['acq_clk_hz']

table = load_arrow_file("memory-monitor_0.arrow")

time_s = table["Clock"].to_numpy() / acq_clk_hz

plt.figure()
plt.plot(time_s, table["PercentUsed"])
plt.xlabel("Time (s)")
plt.ylabel("FIFO used (%)")
plt.title("Hardware Buffer Usage")
plt.show()
```

### Plotting with pandas

Converting the Arrow table to a pandas DataFrame gives access to pandas's `.plot()` method and
column-based indexing, which can make exploratory analysis more concise. The pandas workflow for
the memory monitor data looks like this:

```python
import pyarrow as pa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from load_arrow import load_arrow_file

dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt("start-time_0.csv", delimiter=',', dtype=dt)
acq_clk_hz = meta['acq_clk_hz']

table = load_arrow_file("memory-monitor_0.arrow")

df["time_s"] = df["Clock"] / acq_clk_hz

fig, axes = plt.subplots(2, 1, sharex=True)

df.plot(
  ax=axes[0],
  x="time_s",
  y="PercentUsed",
  ylabel="FIFO used (%)",
  legend=False)

df.plot(
  ax=axes[1],
  x="time_s",
  y="BytesUsed",
  xlabel="Time (s)",
  ylabel="Bytes used",
  legend=False)

plt.tight_layout()
plt.show()
```

> [!IMPORTANT]
> Calling `.to_pandas()` can copy the entire table into RAM, potentially exceeding
> memory usage limits. For short recordings this is a convenient workflow, but for large files on
> memory-limited machines, prefer working directly with the PyArrow table as shown above.

## Advanced Arrow Topics

### What is the Apache Arrow file format?

Apache Arrow files organize data in a
[column-oriented](https://en.wikipedia.org/wiki/Data_orientation#Column-oriented)
layout optimized for operations typical in time-series analysis, such as
filtering, grouping, and aggregation. Concretely, samples from a single data
source, e.g. a single electrophysiology channel, are stored next to each other
on disk. This means an analysis tool can read just the channels it needs without
first rearranging or copying the contents of the file after it has been loaded
into memory. Additionally, each file is self-describing: it opens with a schema that
declares every column's name and data type, followed by a sequence of [record
batches](https://arrow.apache.org/docs/format/Glossary.html#term-record-batch).
Each record batch is a group of rows in which each column's values are stored as
a contiguous array. Unlike plain text data formats
(e.g. CSV files produced by
[CsvWriter](https://bonsai-rx.org/docs/api/Bonsai.IO.CsvWriter.html)) or flat
binary files (e.g. files produced by
[MatrixWriter](https://bonsai-rx.org/docs/api/Bonsai.Dsp.MatrixWriter.html)),
Arrow files contain data type information (e.g., 16-bit integers, 64-bit
floating point numbers, etc.), and do not require a separate metadata file or
prior knowledge of the data layout in order to be loaded correctly.

> [!NOTE]
> To convert from Arrow files to a format similar to the output of `CsvWriter` or `MatrixWriter`,
> check out [this section](#converting-to-other-formats) for details on how to convert the data into
> other formats.

### How data is written

`DataFrameWriter` does not write one row to disk per incoming frame. Instead, it
accumulates frames into an in-memory buffer and writes them to disk as a single
record batch. The target buffer size is determined automatically by the data
frame type and is not user-configurable. The data in the buffer is written to
disk when it reaches that size or after at most five seconds, whichever comes
first.

This batching strategy keeps disk I/O efficient without placing any special
requirements on your workflow structure.

### Manually Loading Arrow Files

The scripts provided in the [loading section](#loading-data-in-python) utilize the [provided
script](#loading-script) to handle loading data without you needing to know any specifics about how
to access the data. In this section, we provide some code snippets that could be used to manually
interact with the Arrow file in cases where the provided script does not meet some need.

#### Memory-mapped loading

The most efficient way to read Arrow files in Python is to open the file as a memory map and pass it
to `pyarrow.ipc.open_file()`. With this approach, PyArrow maps the file into the process's virtual
address space and reads data on demand rather than copying the entire file into RAM upfront. For large
recordings, this is significantly more memory-efficient than loading everything at once.

```python
import pyarrow as pa

with pa.memory_map("memory-monitor_0.arrow", "r") as source:
    with pa.ipc.open_file(source) as reader:
        print(f"Schema: {reader.schema}")
        print(f"Number of record batches: {reader.num_record_batches}")
        table = reader.read_all()
```

Individual record batches can be read one at a time, which is useful when you only need a subset of
the data or when the full recording does not fit in available RAM:

```python
import pyarrow as pa

with pa.memory_map("memory-monitor_0.arrow", "r") as source:
    with pa.ipc.open_file(source) as reader:
        for i in range(reader.num_record_batches):
            batch = reader.get_batch(i)
            # Process individual batch
```

It is also possible to load a specific range of record batches into a table to
analyze a fixed time window without loading the full recording. In the following
snippet, the first 10 record batches are loaded.

```python
import pyarrow as pa

with pa.memory_map("memory-monitor_0.arrow", "r") as source:
    with pa.ipc.open_file(source) as reader:
        indices = range(10) # Make sure the range does not exceed reader.num_record_batches
        table = pa.Table.from_batches(reader.get_batch(i) for i in indices)
```

### Loading and recovering corrupt files

If a power outage or other unforeseen event occurs during recording and leaves
the file in a state where it cannot be opened by the example scripts above, the
following scripts can be used to recover a file that has closed exceptionally.

> [!NOTE]
> Data durability was a *first class requirement* when selecting the Arrow file
> format. Worst case data loss is a single record batch. For high-bandwidth
> sources like Neuropixels, `DataFrameWriter` produces record batches that are
> 1 second in duration. For low-bandwidth or aperiodic sources, it flushes its
> input buffer to disk every 5 seconds. Data written before any interruption
> (unhandled exception, out-of-memory condition, power outage, etc.) can always
> be recovered.

#### Recovering an Arrow file with invalid footer

If recording is interrupted, the file may be missing the footer that Arrow uses to index record
batches, causing PyArrow to raise `ArrowInvalid: Not an Arrow file` when you try to open it. This
script works around the missing footer by opening the file as an Arrow Stream rather than an Arrow
File. The Stream format reads record batches sequentially without relying on the footer, so all
batches written before the interruption can still be recovered. The recovered batches are then
written to a new file, which automatically generates a valid footer on close.

[!code-python[](../../scripts/tutorials/data-frame-writer/recover-invalid-footer.py)]

#### Recovering an Arrow file with corrupted batches

This script reads an Arrow file with an intact footer that has been corrupted in some other way
(invalid buffers, corrupted headers, etc.) and writes all valid batches to a new file. One error
that indicates the buffers or headers have been corrupted is `ArrowInvalid: Unexpected empty message
in IPC file format`.

> [!WARNING] 
> This script will discard any batches that have an error without attempting to correct
> the error, leading to skips in the data. The `Clock` column can be inspected afterward to identify
> gaps where batches were skipped.

[!code-python[](../../scripts/tutorials/data-frame-writer/recover-corrupted-batches.py)]

#### Handling compressed data

If the corrupt data file was originally saved with compression and you want to
re-save the recovered data with compression, pass an `IpcWriteOptions` object to
`pa.ipc.new_file()`. The example below applies Zstandard compression, which is
the same algorithm used by `DataFrameWriter` when `EnableCompression` is `True`.
The change is the same for both recovery scripts above; this example uses the
[invalid footer](#recovering-an-arrow-file-with-invalid-footer) script:

[!code-python[](../../scripts/tutorials/data-frame-writer/recover-compressed-data.py)]


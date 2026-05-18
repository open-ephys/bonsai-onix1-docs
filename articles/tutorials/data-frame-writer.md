---
uid: data-frame-writer
title: Writing Data with DataFrameWriter
---

The <xref:OpenEphys.Onix1.DataFrameWriter.DataFrameWriter> operator provides a straightforward way to
save ONIX data to disk in the [Apache Arrow IPC file
format](https://arrow.apache.org/docs/format/Columnar.html#ipc-file-format). This format is
columnar, self-describing, and natively supported by many scientific Python libraries. This tutorial
explains how to add `DataFrameWriter` to an acquisition workflow, configure its properties
(including optional compression), and efficiently load the resulting files in Python.

> [!NOTE]
> If you are not familiar with the basic usage of the `OpenEphys.Onix1` library, visit the [Getting
> Started](xref:getting-started) guide to set up your Bonsai environment and familiarize yourself
> with using the library to acquire data from ONIX before proceeding.

## What Is the Apache Arrow File Format?

Apache Arrow IPC files store data in a column-oriented layout that aligns naturally with how neural
data is typically analyzed; that is, operating on all values from a single channel or field across time
rather than row by row. Each file contains a schema that describes its columns and a sequence of
record batches, which are fixed-size groups of rows. Unlike CSV files, Arrow files preserve native
data types (e.g., 16-bit integers, 64-bit floating point), which eliminates the need for manual type
conversion when loading data. See the [code snippets](#loading-data-in-python) below to see how to
preserve data types during conversion between different formats.

Arrow files are readable by [PyArrow](https://arrow.apache.org/docs/python/index.html) and any
library built on top of it, including [pandas](https://pandas.pydata.org/),
[numpy](https://numpy.org/) and [Polars](https://pola.rs/), among others.

## Adding DataFrameWriter to a Workflow

`DataFrameWriter` is a sink operator that accepts any device data stream that produces
<xref:OpenEphys.Onix1.DataFrame> or <xref:OpenEphys.Onix1.BufferedDataFrame> elements. In practice,
this means it can be placed downstream of virtually any ONIX <xref:dataio>.

You can use multiple `DataFrameWriter` nodes in the same workflow, placing one per data stream. Give each
node a descriptive `FileName` so recordings are easy to identify after the fact.

::: workflow
![/workflows/tutorials/data-frame-writer/data-frame-writer-example workflow](../../workflows/tutorials/data-frame-writer/data-frame-writer-example.bonsai)
:::

### Operator Properties

Check out the <xref:OpenEphys.Onix1.DataFrameWriter.DataFrameWriter> page to see what properties are available for editing. 

## How Data Is Written

`DataFrameWriter` does not write one row to disk per incoming frame. Instead, it accumulates frames
into an in-memory buffer and writes them to disk as a single record batch. The buffer is flushed
when it reaches its target size or after at most five seconds, whichever comes first. 

This batching strategy keeps disk I/O efficient without placing any special requirements on your
workflow structure.

## Compression

Setting `EnableCompression` to `True` instructs `DataFrameWriter` to compress each record batch
using the [Zstandard (Zstd)](https://facebook.github.io/zstd/) codec before writing it to disk. Zstd
is a general-purpose compression algorithm that offers a good balance between compression ratio and
speed. For typical neural data, enabling compression can substantially reduce file sizes.

### When to Enable Compression

Enable compression when storage space is a constraint and the additional CPU load during acquisition
is acceptable. Compression runs on the same machine that is acquiring data, so it competes with the
rest of your acquisition pipeline for CPU resources. For most workloads this overhead is negligible,
but for very high-bandwidth configurations (e.g., multiple Neuropixels probes) or when running other
computationally intensive processing in the same workflow, benchmark your system before relying on
compression in long recordings.

> [!TIP]
> A practical way to evaluate the impact of compression on your specific setup is to run the [Load
> Tester](xref:tune-readsize) workflow alongside a `DataFrameWriter` with `EnableCompression` set
> to `True` and compare the hardware buffer usage against a run without compression. If the
> `PercentUsed` value remains near zero in both cases, compression is a feasible option to use in your
> configuration.

### Loading Compressed Files

You do not need to know whether a file was written with compression enabled in order to load it.
PyArrow reads the compression metadata stored in each record batch header and decompresses the data
automatically. The loading code shown in the [next section](#loading-data-in-python) works
identically for both compressed and uncompressed files.

The only difference is time: loading a compressed file requires decompressing each record batch
before the data can be used, which adds CPU work that is not present when loading an uncompressed
file. For analysis of large recordings this additional latency may be noticeable,
especially on machines with slower CPUs. If fast random access to large files is a priority, prefer
uncompressed files.

## Loading Data in Python

### Installation

To follow along with the examples in this tutorial, you will need to install python, pyarrow, and
pandas if you have not already. Once python is installed, run the following command to install the
python packages:

```
pip install pyarrow pandas matplotlib
```

To run `matplotlib`, you will also need to install a backend to plot and interact with the figures.
See their documentation page
[here](https://matplotlib.org/stable/users/explain/figure/backends.html) for more details on how to
install and connect to different backends.

### Memory-Mapped Loading (Recommended)

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

It is also possible to load a range of record batches into a table, to maintain consistency with any
processing pipelines:

```python
import pyarrow as pa

with pa.memory_map("memory-monitor_0.arrow", "r") as source:
    with pa.ipc.open_file(source) as reader:
        indices = range(10) # Ensure the range chosen is less than the total number of record batches
        table = pa.Table.from_batches(reader.get_batch(i) for i in indices)
```

### Converting to a pandas DataFrame

If your analysis uses pandas, you can convert an Arrow Table to a DataFrame by calling `.to_pandas()`:

```python
import pyarrow as pa
import pandas as pd

with pa.memory_map("memory-monitor_0.arrow", "r") as source:
    with pa.ipc.open_file(source) as reader:
        table = reader.read_all()
        df = table.to_pandas(types_mapper=pd.ArrowDtype)
```

> [!IMPORTANT]
> Calling `.to_pandas()`, or any other method that converts the table to a pandas DataFrame, might
> copy the entire dataset into RAM. Pandas and PyArrow can, in certain limited circumstances,
> maintain memory mapping across boundaries, but it is not guaranteed. Keep this in mind when
> working with long recordings on machines with limited memory.

### Using pandas Directly

It is also possible to load an Arrow file directly with
[`pandas.read_feather()`](https://pandas.pydata.org/docs/reference/api/pandas.read_feather.html):

```python
import pandas as pd

df = pd.read_feather("memory-monitor_0.arrow", dtype_backend="pyarrow")
```

This is convenient for short recordings, but it calls PyArrow internally and loads the entire file
into RAM regardless of how large it is. It also does not expose batch-level access, so there is no
way to read only a portion of the recording without first loading the whole thing. For large or long
recordings, the memory-mapped approach described above is preferable.

## Plotting Data in Python

This section shows how to plot data saved from a `MemoryMonitor` device. Its schema contains four
columns: `Clock`, `HubClock`, `PercentUsed`, and `BytesUsed`. The `Clock` column records the raw
acquisition clock count and must be divided by the acquisition clock rate to produce a time value in
seconds.

### Reading the Acquisition Clock Rate

The acquisition clock rate is written to a `start-time_<suffix>.csv` file whenever the example
acquisition workflow runs. Load it with NumPy before plotting:

```python
import numpy as np

dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt("start-time_0.csv", delimiter=',', dtype=dt)
acq_clk_hz = meta['acq_clk_hz']
```

### Plotting Directly from a PyArrow Table

PyArrow column arrays implement the [Python array
protocol](https://arrow.apache.org/docs/python/numpy.html), so most plotting libraries, including
Matplotlib, can consume them directly without an explicit conversion step. The `Clock` column is an
exception: arithmetic operations such as dividing by the clock rate require a call to `.to_numpy()`
first to produce a NumPy array.

```python
import pyarrow as pa
import numpy as np
import matplotlib.pyplot as plt

dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt("start-time_0.csv", delimiter=',', dtype=dt)
acq_clk_hz = meta['acq_clk_hz']

with pa.memory_map("memory-monitor_0.arrow", "r") as source:
    with pa.ipc.open_file(source) as reader:
        table = reader.read_all()

time_s = table["Clock"].to_numpy() / acq_clk_hz

plt.figure()
plt.plot(time_s, table["PercentUsed"])
plt.xlabel("Time (s)")
plt.ylabel("FIFO used (%)")
plt.title("Hardware Buffer Usage")
plt.show()
```

Working directly with the table means that as long as PyArrow keeps the file memory-mapped, only
the columns you access are paged into RAM. No intermediate copy of the full dataset is made unless
you explicitly request one.

> [!NOTE]
> If the recording is too large to hold in memory at once, read and plot subsets of record batches
> using `reader.get_batch(i)` and call `plt.plot()` incrementally instead of calling
> `reader.read_all()`. This keeps peak memory usage proportional to the size of a single batch
> rather than the full recording.

### Plotting with pandas

Converting the Arrow table to a pandas DataFrame gives access to pandas's `.plot()` method and
column-based indexing, which can make exploratory analysis more concise. The pandas workflow for
the memory monitor data looks like this:

```python
import pyarrow as pa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dt = {'names': ('time', 'acq_clk_hz', 'block_read_sz', 'block_write_sz'),
      'formats': ('datetime64[us]', 'u4', 'u4', 'u4')}
meta = np.genfromtxt("start-time_0.csv", delimiter=',', dtype=dt)
acq_clk_hz = meta['acq_clk_hz']

with pa.memory_map("memory-monitor_0.arrow", "r") as source:
    with pa.ipc.open_file(source) as reader:
        table = reader.read_all()
        df = table.to_pandas(types_mapper=pd.ArrowDtype)

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
> Calling `.to_pandas()` can copy the entire table into RAM, potentially doubling
> memory usage. For short recordings this is a convenient workflow, but for large files on
> memory-limited machines, prefer working directly with the PyArrow table as shown above.

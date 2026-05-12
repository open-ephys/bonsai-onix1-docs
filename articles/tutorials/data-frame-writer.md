---
uid: data-frame-writer
title: Writing Data with DataFrameWriter
---

The <xref:OpenEphys.Onix1.DataFrameWriter.DataFrameWriter> operator provides a straightforward way to
save ONIX data to disk in the [Apache Arrow IPC file
format](https://arrow.apache.org/docs/format/Columnar.html#ipc-file-format). This format is
columnar, self-describing, and natively supported by many scientific Python libraries. This tutorial
explains how to add `DataFrameWriter` to an acquisition workflow, how to configure its properties
(including optional compression), and how to efficiently load the resulting files in Python.

> [!NOTE]
> If you are not familiar with the basic usage of the `OpenEphys.Onix1` library, visit the [Getting
> Started](xref:getting-started) guide to set up your Bonsai environment and familiarize yourself
> with using the library to acquire data from ONIX before proceeding.

## What Is the Apache Arrow File Format?

Apache Arrow IPC files store data in a column-oriented layout that aligns naturally with how neural
data is typically analyzed. namely operating on all values from a single channel or field across time
rather than row by row. Each file contains a schema that describes its columns and a sequence of
record batches, which are fixed-size groups of rows. Unlike CSV files, Arrow files preserve native
data types (e.g., 16-bit integers, 64-bit floating point), which eliminates the need for manual type
conversion when loading data. See the [code snippets](#loading-data-in-python) below to see how to
preserve data types during conversion between different formats.

Arrow files are readable by [PyArrow](https://arrow.apache.org/docs/python/index.html) and any
library built on top of it, including [pandas](https://pandas.pydata.org/) and
[Polars](https://pola.rs/), among others.

## Adding DataFrameWriter to a Workflow

`DataFrameWriter` is a sink operator that accepts any device data stream that produces
<xref:OpenEphys.Onix1.DataFrame> or <xref:OpenEphys.Onix1.BufferedDataFrame> elements. In practice,
this means it can be placed downstream of virtually any ONIX data I/O operator.

To add `DataFrameWriter` to your workflow:

1. Click on a data acquisition operator (e.g.,
   <xref:OpenEphys.Onix1.MemoryMonitorData>, <xref:OpenEphys.Onix1.NeuropixelsV1eData>, or
   <xref:OpenEphys.Onix1.AnalogInput>) to select it.
2. Navigate to the toolbox to search modules (or press <kbd>Ctrl + E</kbd>), and type `DataFrameWriter`. Select
   <xref:OpenEphys.Onix1.DataFrameWriter.DataFrameWriter> from the results. The operator will be
   connected to the data acquisition operator.
3. Click on `DataFrameWriter` to open its property editor.

> [!TIP]
> You can use multiple `DataFrameWriter` nodes in the same workflow, placing one per data stream. Give each
> node a descriptive `FileName` so recordings are easy to identify after the fact.

## Operator Properties

| Property | Description |
| --- | --- |
| `FileName` | The path and base name for the output file (e.g., `memory-monitor_.arrow`). |
| `Suffix` | A string appended to `FileName` before the extension to distinguish files across runs. Set this to `FileCount` so that each acquisition session produces a numbered file (e.g., `memory-monitor_0.arrow`, `memory-monitor_1.arrow`). |
| `Overwrite` | If `True`, an existing file at the same path is overwritten when the workflow starts. If `False`, an error is raised instead. |
| `Buffered` | Controls whether the file stream buffers data on a separate thread from data acquisition. Leave this at its default (`True`) unless you have a specific reason to disable it. |
| `EnableCompression` | Enables Zstandard (Zstd) compression for the written file. Defaults to `False`. See [Compression](#compression) for guidance. |

### Recommended File Naming

Follow the convention used in the [example hardware workflows](xref:hs64_workflow): set `Suffix` to
`FileCount` and include a trailing underscore in `FileName` (e.g., `memory-monitor_.arrow`). The operator
then produces files like `memory-monitor_0.arrow`, `memory-monitor_1.arrow`, and so on, making it straightforward
to load a specific session from a directory that contains multiple recordings.

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

Install PyArrow if you have not already:

```
pip install pyarrow
```

### Memory-Mapped Loading (Recommended)

The most efficient way to read Arrow files in Python is to open the file as a memory map and pass it
to `pyarrow.ipc.open_file()`. With this approach, PyArrow maps the file into the process's virtual
address space and reads data on demand rather than copying the entire file into RAM upfront. For large
recordings, this is significantly more memory-efficient than loading everything at once.

```python
import pyarrow as pa

source = pa.memory_map("memory-monitor_0.arrow", "r")
reader = pa.ipc.open_file(source)

print(f"Schema: {reader.schema}")
print(f"Number of record batches: {reader.num_record_batches}")

table = reader.read_all()
```

Individual record batches can be read one at a time, which is useful when you only need a subset of
the data or when the full recording does not fit in available RAM:

```python
import pyarrow as pa

source = pa.memory_map("memory-monitor_0.arrow", "r")
reader = pa.ipc.open_file(source)

for i in range(reader.num_record_batches):
    batch = reader.get_batch(i)
    # Process individual batch
```

It is also possible to load a range of record batches into a table, to maintain consistency with any
processing pipelines:

```python
import pyarrow as pa

source = pa.memory_map("memory-monitor_0.arrow", "r")
reader = pa.ipc.open_file(source)

indices = range(100)

table = pa.Table.from_batches(reader.get_batch(i) for i in indices)
```

### Converting to a pandas DataFrame

If your analysis uses pandas, you can convert an Arrow Table to a DataFrame by calling `.to_pandas()`:

```python
import pyarrow as pa
import pandas as pd

source = pa.memory_map("memory-monitor_0.arrow", "r")
reader = pa.ipc.open_file(source)
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

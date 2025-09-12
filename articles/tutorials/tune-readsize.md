---
uid: tune-readsize
title: Optimizing Closed Loop Performance
---

<-- Data between hardware and software is transmitted in buffers, that are xxx. require read and write operations. These take time, overhead. Performance is a tradeoff: smaller chunks of data will get to the host pc faster so we can process them. but if data is processed in small chunks, more operations are needed, creating more overhead. too many read operations increase processing time, negatively impacting performance. I guess this is below more technically once concepts are explained, but still -->

This tutorial shows how to optimize the
<xref:OpenEphys.Onix1.StartAcquisition>'s
<xref:OpenEphys.Onix1.StartAcquisition.ReadSize> property for your specific data
acquisition setup to minimize delays between data collection and computer
processing. This tutorial provides a method to tune `ReadSize` within the 
context of your particular data sources and computer specifications in order to 
achieve the fastest possible response times for closed-loop experiments. In most
situations, sub-200 microsecond closed-loop response times can be achieved.

<-- why don't the write operations matter? i.e. i understand we tune the read to get better read/write (closed-loop) -->

> [!NOTE]
> Performance will vary based on your computer's capabilities and your results
> might differ those presented below. The computer used to create this tutorial
> has the following specs:
> - CPU: Intel i9-12900K
> - RAM: 64 GB
> - GPU: NVIDIA GTX 1070 8GB
> - OS: Windows 11

## Data transmission from ONIX Hardware to Host Computer software

<-- this first paragraph is about hardware buffer but the procedure is about what is happening on the host pc. I would introduce the hardware buffer after the procedure. or better yet, give the takeaways first (see below) -->

The ONIX **Hardware Buffer** consists of 2GB of dedicated RAM
that belongs to the acquisition hardware (it is _not_ RAM in the host computer).
The hardware buffer can be used to temporarily store data that has not yet been transferred to
the host. When the host software is consuming data optimally, the hardware
buffer is bypassed entirely and data flows directly from production to the host 
computer's RAM, minimizing the latency between data collection and processing.

<-- does this minimize? actually below the hw buffer bypass scenario is not the one with lower latencies. It's the one in which the buffer is used properly without overflow (doubt1) -->

Each time the host computer software reads data from the ONIX hardware, it obtains an amount 
**ReadSize** of bytes of data using the following procedure:

<-- Not sure how much they need to know the exact procedure, perhaps the key takeaways first, then the explanation. -->
<-- The takeaways should be what is needed to follow the tutorial. The other explanation they might skip through. -->

1. A block of memory that is `ReadSize` bytes long is allocated on the host by 
   the API for the purpose of holding incoming data from ONIX hardware.
2. A pointer to that memory is provided to the 
   [RIFFA](https://open-ephys.github.io/ONI/v1.0/api/liboni/driver-translators/riffa.html) 
   driver (the PCIe backend of the ONIX system) which moves the allocated memory
   block into a more privileged state known as kernel mode so that it can 
   initiate a 
   [DMA transfer](https://en.wikipedia.org/wiki/Direct_memory_access). DMA 
   allows data transfer to be performed by ONIX hardware without additional CPU 
   intervention.
3. The data transfer completes once `ReadSize` bytes have been produced.
4. The RIFFA driver moves the memory block from kernel mode to user mode so that it 
   can be accessed by software. The API function returns with a pointer to the 
   filled buffer.

The key take-away points about this process are:

1. Memory is allocated only once by the API, and the transfer is
   [zero-copy](https://en.wikipedia.org/wiki/Zero-copy). ONIX hardware writes
   directly into the API-allocated buffer autonomously using minimal resources 
   from the host computer. Within this process, `ReadSize` determines the amount 
   of data that is transferred each time the API reads data from the hardware.
2. If the buffer is allocated and the transfer is initiated by the host API 
   before data is produced by the hardware, the data is transferred directly 
   into the software buffer and completely bypasses the Hardware Buffer. In this 
   case, hardware is literally streaming data to the software buffer _the moment
   it is produced_. It is physically impossible to achieve lower latencies than 
   this situation. The goal of this tutorial is to allow your system to operate 
   in this regime.

<-- but actually below the hw buffer bypass scenario is not the one with lower latencies. It's the one in which the buffer is used properly without overflow (same doubt1) -->

The size of hardware-to-host data transfers is determined by the
<xref:OpenEphys.Onix1.StartAcquisition.ReadSize> property of the
StartAcquisition operator which is in every Bonsai workflow that uses
<xref:OpenEphys.Onix1> to acquire data from ONIX. Choosing an optimal `ReadSize`
value balances the tradeoff between latency and overall bandwidth. Smaller
`ReadSize` values mean that less data is required before the RIFFA driver
relinquishes control of the buffer to software. This, in effect, means software 
can start operating on data closer to the time that the data was produced, and 
thus lower-latency feedback loops can be achieved. However, each data transfer 
requires calls to the RIFFA driver which incurs significant overhead. If 
`ReadSize` is so low that it takes less time for the hardware to produce a 
`ReadSize` amount of data than the average time it takes for the host computer 
to read a `ReadSize` amount of data, the Hardware Buffer will excessively
accumulate data. This will destroy real-time performance and eventually cause 
the hardware buffer to overflow, terminating acquisition.

## Tuning `ReadSize` to Optimize Closed Loop Performance
ONIX provides a mechanism for tuning the value of `ReadSize` to optimize closed
loop performance that takes into account the idiosyncrasies of your host
computer and experimental acquisition setup.

> [!NOTE]
> If you are not familiar with the basic usage of the `OpenEphys.Onix1` library,
> then visit the [Getting Started](xref:getting-started) guide to set up your
> Bonsai environment and familiarize yourself with using the library to acquire
> data from ONIX before proceeding.

Copy the following workflow into the Bonsai workflow editor by hovering over
workflow image and clicking on the clipboard icon that appears. Open Bonsai and
paste this workflow by clicking the Bonsai workflow editor pane and pressing
<kbd>Ctrl+V</kbd>.

::: workflow
![SVG of load tester workflow](../../workflows/tutorials/tune-readsize/tune-readsize.bonsai)
:::

<-- why not use the actual experimental hardware instead of the load tester? -->

### Hardware Configuration
The top-row configuration chain includes a
<xref:OpenEphys.Onix1.ConfigureLoadTester> operator. This configures ONIX's Load
Tester Device, which produces and consumes data at user-specified rates for
testing and tuning the latency between data production and real-time feedback.
This device is _not a emulator_. It is a real hardware device that produces and
consumes data using the selected driver and physical link (e.g. PCIe bus) and
thus provides accurate measurements of feedback performance for a given host
computer.

::: workflow
![SVG of load tester workflow configuration chain](../../workflows/tutorials/tune-readsize/configuration.bonsai)
:::

We need to configure the load tester to produce and consume the same amount of
data as our real experimental hardware would. For example, lets say that during
our closed loop experiment, feedback signals will be generated as a function of
data acquired from two Neuropixels 2.0 probes, each of which generates a 384
channel sample at 30 kHz. The overall bandwidth is

<-- explain where the 2 bytes per sample comes from -->

$$
\begin{equation}
  2\,probes*\frac{384\,chan.}{probe}*\frac{30\,ksamp.}{sec\,chan.}*\frac{2\,bytes}{samp.} \approx 47\,MB/s
  \label{eq:2xnpx2bw}
\end{equation}
$$

We'll setup `ConfigureLoadTester` to produce data at the same frequency and
bandwidth as two Neuropixels 2.0 probes with the following settings:

<img style="float: right; margin-bottom: 1rem" src="../../images/tutorials/tune-readsize/load-tester-configuration_properties-editor.webp" alt="screenshot of ConfigureLoadTester's property editor">

- `DeviceAddress` is set to 11 because that's how this device is indexed in the
  ONIX system.
- `DeviceName` is set to "Load Tester"
- `Enable` is set to True to enable the LoadTester device.
- `FramesPerSecond` is then set to 60,000 Hz. The rate at which frames are
  produced by two probes, since each is acquired independently.
- `ReceivedWords` is set to 392 bytes, the size of a single
  <xref:OpenEphys.Onix1.NeuropixelsV2eDataFrame>, which includes xx extra bytes besides the neuropixels data.
- `TransmittedWords` is set to 100 bytes. This simulates the amount of data
  required to e.g. send a stimulus waveform.

> [!NOTE]
> The `DeviceAddress` must be manually configured because
> <xref:OpenEphys.Onix1.ConfigureLoadTester> is used for diagnostics and testing
> and therefore is not made available through
> <xref:OpenEphys.Onix1.ConfigureBreakoutBoard> like the rest of the local
> devices (analog IO, digital IO, etc.)
<-- so how to find device addresses? -->


Next we configure <xref:OpenEphys.Onix1.StartAcquisition>'s
<xref:OpenEphys.Onix1.StartAcquisition.ReadSize>
<xref:OpenEphys.Onix1.StartAcquisition.WriteSize> properties.

<-- WriteSize also exists. it is this. we set it to xx. because of... -->

`WriteSize` is set
to 16384 bytes. This defines a readily-available pool of memory for the creation
of output data frames. A larger size will reduce the frequency of dynamic memory
allocation system calls but increase the expense of each of those calls. The
effect on real-time performance is typically not as large as that of the
`ReadSize` property because it does not determine when data is written to
hardware. Data is written to hardware as soon as an output frame has been
created. To start, we also set the `ReadSize` property is also set to 16384. 
Later in this tutorial, we'll examine the effect of this value on real-time
performance.

### Real-time Loop

The bottom half of the workflow is used to stream data back to the load testing
device from hardware so that it can perform a measurement of round trip latency.
The <xref:OpenEphys.Onix1.LoadTesterData> operator acquires a sequence of
[LoadTesterDataFrames](xref:OpenEphys.Onix1.LoadTesterDataFrame) from the
hardware each of which is split into its
<xref:OpenEphys.Onix1.DataFrame.HubClock> member and
<xref:OpenEphys.Onix1.LoadTesterDataFrame.HubClockDelta> member.

::: workflow
![SVG of load tester workflow loadtester branch](../../workflows/tutorials/tune-readsize/loadtester.bonsai)
:::

The `HubClock` member indicates the acquisition clock count when the
`LoadTesterDataFrame` was produced. The `EveryNth` operator is a
<xref:Bonsai.Reactive.Condition> operator which only allows through every Nth 
element in the observable sequence. This is used to simulate an algorithm, such 
as spike detection, that only triggers closed loop feedback in response to input
data meeting some condition. The value of `N` can be changed to simulate 
different feedback frequencies. You can inspect its logic by double-clicking the
node when the workflow is not running. In this case, `N` is set to 100, so every
100th sample is delivered to <xref:OpenEphys.Onix1.LoadTesterLoopback>.

`LoadTesterLoopback` is a *sink* which writes HubClock values it receives back 
to the load tester device. When the load tester device receives a HubClock from 
the host computer, it's subtracted from the current acquisition clock count. 
That difference is sent back to the host computer as the `HubClockDelta` 
property of subsequent `LoadTesterDataFrames`. In other words, `HubClockDelta` 
indicates the amount of time that has passed since the creation of a frame in 
hardware and the receipt of a feedback signal in hardware based on that frame: 
it is a complete measurement of closed loop latency. This value is converted to 
milliseconds and then <xref:Bonsai.Dsp.Histogram1D> is used to to help visualize
the distribution of closed-loop latencies.

Finally, at the bottom of the workflow, a
<xref:OpenEphys.Onix1.MemoryMonitorData> operator is used to examine the state
of the hardware buffer. To learn about the
<xref:OpenEphys.Onix1.MemoryMonitorData> branch, visit the [Breakout Board
Memory Monitor](xref:breakout_memory-monitor) page.

::: workflow
![SVG of load tester workflow memorymonitor branch](../../workflows/tutorials/tune-readsize/memory-monitor.bonsai)
:::

### Real-time Latency for Different `ReadSize` Values

#### `ReadSize` = 16384 bytes
With `ReadSize` set to 16384 bytes, start the workflow, and
[open the visualizers](xref:visualize-data) for the PercentUsed and Histogram1D
nodes:

![screenshot of Histogram1D visualizers with `ReadSize` 16384](../../images/tutorials/tune-readsize/histogram1d_16384.webp)
![screenshot of PercentUsed visualizers with `ReadSize` 16384](../../images/tutorials/tune-readsize/percent-used_16384.webp)

Since data is produced at about 47MB/s, it takes about 340 μs to produce 16384 
bytes of data. This means that the data contained in a single `ReadSize` block 
was generated in the span of approximately 340 μs.

<-- from here -->

Because we are using every 
100th sample to generate feedback, the sample that is actually used to trigger 
an output could be any from that 340 μs span resulting in latencies that are 
lower then 340 μs. This is reflected in the Histogram1D visualizer.

<-- to here, i think this explains why it is variable, which is a separate point. in my chain of thought i wanted to hear about the 300mus first -->

The average latency is ~300 μs

<-- potentially what the plots are and the three things we will look at (average, variability, y scale) can be explained above before starting the three cases -->

(in this plot, 1000 corresponds to 1 ms) <-- would it be clearer to say: the y axis is in mus ? -->

and can be as low as
~60 μs. The long tail in the distribution corresponds to instances when the
hardware buffer was used or the operating system was busy with other tasks.

With `ReadSize` of 16384 bytes, the PercentUsed visualizer shows that the
percent of the Hardware Buffer being used remains close to zero. This indicates 
that the Hardware Buffer is generally being bypassed because data is being read 
more quickly by the host than it is produced by the hardware. For experiments 
without hard real-time constraints, this latency is perfectly acceptable. For 
experiments with hard real-time constraints, let's see how low we can get the 
closed-loop latency.

#### `ReadSize` = 2048 bytes
Set `ReadSize` to 2048 bytes, restart the workflow (`ReadSize` is a
[<button class="badge oe-badge-border oe-badge-yellow" data-bs-toggle="tooltip" title="Configuration properties have an effect on hardware when a workflow is started and are used to initialize the hardware state. If they are changed while a workflow is running, they will not have an effect until the workflow is restarted."> Configuration</button>](xref:OpenEphys.Onix1#configuration)
property so it only updates when a workflow starts), and open the same visualizers:

![screenshot of Histogram1D visualizers with `ReadSize` 2048](../../images/tutorials/tune-readsize/histogram1d_2048.webp)
![screenshot of PercentUsed visualizers with `ReadSize` 2048](../../images/tutorials/tune-readsize/percent-used_2048.webp)

The closed-loop latencies now average about 80 μs. The hardware buffer is still
stable at around around zero indicating that, even given the increased overhead
associated with a smaller `ReadSize`, software is collecting data rapidly enough
to prevent excessive accumulation in the hardware buffer. Let's see if we can 
decrease latency even further.

#### `ReadSize` = 1024 bytes

Set `ReadSize` to 1024 bytes, restart the workflow, and open the same visualizers.

![screenshot of Histogram1D visualizers with `ReadSize` 1024](../../images/tutorials/tune-readsize/histogram1d_1024.webp)
![screenshot of PercentUsed visualizers with `ReadSize` 1024](../../images/tutorials/tune-readsize/percent-used_1024.webp)

The Histogram1D visualizer appears to be empty. This is because the latency
immediately exceeds the x-axis upper limit of 1 ms. You can see this by
inspecting the visualizer for the node prior to Histogram1D. Because of the very
small buffer size (which is on the order of a single Neuropixel 2.0 sample), the 
computer cannot perform read operations at a rate required to keep up with data
production. This causes excessive accumulation of data in the hardware buffer. 
The most recently produced data is added to the end of the hardware buffer's 
queue, requiring several read operations before it can be read. As more data 
accumulates in the buffer, the duration of time from when that data was produced
and when that data can finally be read increases. In other words, latencies 
increase dramatically, and closed loop performance collapses.

Because the amount of data in the hardware buffer is increasing (which is 
indicated by the steadily rising PercentUsed visualizer), the acquisition 
session will eventually terminate in an error when the MemoryMonitor PercentUsed
reaches 100% and the hardware buffer overflows.

#### Summary

The results of our experimentation are as follows:

| `ReadSize`  | Latency        | Buffer Usage   | Notes                                                                                              |
|-------------|----------------|----------------|----------------------------------------------------------------------------------------------------|
| 16384 bytes | ~300 μs        | Stable at 0%   | Perfectly adequate if there are no strict low latency requirements, lowest risk of buffer overflow |
| 2048 bytes  | ~80 μs         | Stable near 0% | Balances latency requirements with low risk of buffer overflow                                     |
| 1024 bytes  | Rises steadily | Unstable       | Certain buffer overflow and terrible closed loop performance                                       |

These results may differ for your experimental system. For example, your system
might have different bandwidth requirements (if you are using different devices,
data is produced at a different rate) or use a computer with different
performance capabilities (which changes how quickly read operations can occur).
For example, here is a similar table made by configuring the Load Tester device
to produce data at a rate similar to a single 64-channel Intan chip (such as
what is on the <xref:hs64>), ~4.3 MB/s:

![screenshot of ConfigureLoadTester's property editor for a single Intan chips](../../images/tutorials/tune-readsize/load-tester-configuration_properties-editor_64ch.webp)

| `ReadSize` | Latency        | Buffer Usage | Notes                                                                             |
|------------|----------------|--------------|-----------------------------------------------------------------------------------|
| 1024 bytes | ~200 μs        | Stable at 0% | Perfectly adequate if that are no strict low latency requirements                 |
| 512 bytes  | ~110 μs        | Stable at 0% | Lower latency, no risk of buffer overflow                                         |
| 256 bytes  | ~80 μs         | Stable at 0% | Lowest achievable latency with this setup, still no risk of buffer overflow       |
| 128 bytes  | -              | -            | Results in error -- 128 bytes is too small for the current hardware configuration |

Regarding the last row of the above table, the lowest `ReadSize` possible is
determined by the size of the largest data frame produced by enabled devices
(plus some overhead). Even with the lowest possible `ReadSize` value, 256 bytes,
there is very little risk of overflowing the buffer. The PercentUsed visualizer
shows that the hardware buffer does not accumulate data:

![](../../images/tutorials/tune-readsize/percent-used_256_lower-payload.png)

These two tables together demonstrates why it is impossible to recommend a
single correct value for `ReadSize` that is adequate for all experiments. The
diversity of experiments (in particular, the wide range at which they produce
data) requires a range of `ReadSize` values.

Last, in this tutorial, there was minimal computational load imposed by
the workflow itself. In most applications, some processing is performed on the 
data to generate the feedback signal. It's important to take this into account 
when tuning your system and potentially modifying the workflow to perform 
computations on incoming data in order to account for the effect of 
computational demand on closed loop performance.

<!-- ## Tuning `ReadSize` with Real-Time Computation -->
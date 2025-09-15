---
uid: data-elements
title: Data Elements
---

Data elements are produced by <xref:OpenEphys.Onix1> Bonsai operators. These
pages contain information about the properties that comprise data elements to
help interpret and load the data produced by a device.

In general, a data element comprises of properties which together contain
timestamped data from a particular device. For example,
<xref:OpenEphys.Onix1.Bno055Data> outputs
[Bno055DataFrames](xref:OpenEphys.Onix1.Bno055DataFrame) which contains data
produced by a BNO055 device: 
-   The data produced by the BNO055 is contained in the Acceleration,
    Calibration, EulerAngle, Gravity, and Temperature properties of the
    Bno055DataFrame. Any of these properties can be individually selected and
    visualized in Bonsai.
-   The <xref:OpenEphys.Onix1.DataFrame.Clock> property contains the precise
    hardware timestamp for the data in the properties described in the 1st
    bullet point generated using the global ONIX Controller clock. This Clock
    property can be used to sync BNO055 data with data from all other devices
    that ONIX is acquiring from onto the same timeline. 
-   The <xref:OpenEphys.Onix1.DataFrame.HubClock> property contains the precise
    hardware timestamp generated using the clock on the hardware that contains
    the device.

There are a few exceptions to the patter described above: 
-   <xref:OpenEphys.Onix1.ContextTask> is an object passed through the
    configuration chain for writing to and reading from the ONIX hardware.
-   <xref:OpenEphys.Onix1.OutputClockParameters> outputs the parameters used to
    set the precise hardware output clock when the workflow starts.

These pages also describe the type of each property. The type information can be
used to calculate the rate of data produced by the devices enabled in your
experiment. For example, the <xref:OpenEphys.Onix1.NeuropixelsV2eData> operator
(which outputs the data produced by a single Neuropixels 2.0 probe device)
produces a sequence of
[NeuropixelsV2eDataFrames](xref:OpenEphys.Onix1.NeuropixelsV2eDataFrame). Using
the fact that each sample comprises of a Clock property (8 bytes), a HubClock
property (8 bytes), and an AmplifierData property (384*2 bytes), the data rate
is: 

$$
\begin{equation}
    \frac{2*384+8+8\,bytes}{sample}*\frac{30,000\,samples}{s}*\frac{1\,MB}{10^6bytes} = 23.52\,MB/s
    \label{eq:1x_npx2_bw}
\end{equation}
$$

NeuropixelsV2eDataFrame is actually a buffered data frame (as indicated by the
presence of NeuropixelsV2eData's BufferSize property), meaning that several data
samples and their timestamps are buffered into a single NeuropixelsV2eDataFrame.
The above calculation was calculated under the assumption that
NeuropixelsV2eData's BufferSize property is set to 1. Although the calculation
is slightly different when BufferSize is more than 1, the end result ends up
being the same. When BufferSize is more than 1, NeuropixelsV2eDataFrames are
produced at a rate 30 kHz divided by the value of BufferSize. Each
NeuropixelsV2eDataFrame comprises of:

-   a Clock property: an array of <a class="xref external"
    href="https://learn.microsoft.com/dotnet/api/system.uint64" target="_blank"
    rel="noopener noreferrer nofollow">ulong</a> (each 8 bytes) of length N
-   a HubClock property: an array of <a class="xref external"
    href="https://learn.microsoft.com/dotnet/api/system.uint64" target="_blank"
    rel="noopener noreferrer nofollow">ulong</a> (each 8 bytes) of length N
-   an AmplifierData property: a <xref:OpenCV.Net.Mat> of <a class="xref
    external" href="https://learn.microsoft.com/dotnet/api/system.uint16"
    target="_blank" rel="noopener noreferrer nofollow">ushort</a> (each 2 bytes)
    of size 384 x N

where N is a stand-in for BufferSize. Therefore, the calculation becomes:

$$
\begin{equation}
    \frac{(2*384+8+8)*N\,bytes}{sample}*\frac{30,000/N\,samples}{s}*\frac{1\,MB}{10^6bytes} = 23.52\,MB/s
    \label{eq:1x_npx2_bw_buffersize}
\end{equation}
$$

N cancels out and the result is the same. 

Knowing the type of each property can also be helpful in two more ways:

-   A property's type indicates how a property can be used in Bonsai. Operators
    typically accept only a specific type or set of types as inputs. When types
    don't match, Bonsai indicates an error.
-   If a property is saved using a <xref:Bonsai.Dsp.MatrixWriter>, its type
    informs how to load the saved file. For example, the dtypes in our 
    [example Breakout Board data-loading script](xref:breakout_load-data) were
    selected to match the size of the data being saved.



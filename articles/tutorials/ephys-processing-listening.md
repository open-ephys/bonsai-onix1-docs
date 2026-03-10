---
uid: ephys-process-listen
title: Process and Listen to Ephys Data
---

This tutorial shows you how to perform basic online signal processing of electrophysiology data in
Bonsai such as channel selection/reordering, frequency filtering, and fixed-threshold spike
detection as well as how to listen to ephys data using ONIX hardware and the OpenEphys.Onix1 Bonsai
package. 

> [!NOTE]
> This tutorial serves primarily as an introduction to basic operations for processing electrophysiology data in Bonsai. These operations can also be performed in the Open Ephys GUI which provides advanced visualizations and built-in processing modules.

<!--To learn how to pipe data to the Open Ephys GUI from Bonsai to leverage
> these features of the Open Ephys GUI, refer to the [Open Ephys Socket
> Tutorial](xref:open-ephys-socket).
 More advanced online processing can be performed in Bonsai with specialized packages.
 -->

<!-- Include the above comment in the note when socket tutorial is deployed -->

::: workflow
![/workflows/tutorials/ephys-process-listen/ephys-process-listen.bonsai workflow](../../workflows/tutorials/ephys-process-listen/ephys-process-listen.bonsai)
:::

> [!TIP]
> This tutorial uses the Headstage 64. To find pertinent information for processing data produced by
> the Intan Rhd2164 ephys device on the Headstage 64 (such as the numbers used to convert DAC data
> to units of voltage), navigate to <xref:OpenEphys.Onix1.Rhd2164DataFrame> which is the page for
> the data element produced by the <xref:OpenEphys.Onix1.Rhd2164Data> operator. The process of
> navigating the reference to find pertinent information is the same for other ephys headstages that
> you might want to use to follow along in this tutorial. It also helps to be familiar with the
> example workflow for your particular hardware available in the <xref:data-acq-quick-start>.

## Get Started in Bonsai

Follow the [Getting Started](xref:getting-started) guide to set up and familiarize yourself with
Bonsai. In particular:

- [Download the necessary Bonsai packages](xref:install-configure-bonsai#install-packages)
or [check for updates](xref:install-configure-bonsai#update-packages) if they're already
installed. This tutorial assumes you're using the latest packages.
- Read about [visualizing data](xref:visualize-data). We recommend verifying each step of the
tutorial by visualizing the data produced.

## Configure the Hardware

Construct a [top-level hardware configuration chain](xref:onix-configuration): 

::: workflow
![/workflows/tutorials/ephys-process-listen/configure.bonsai workflow](../../workflows/tutorials/ephys-process-listen/configure.bonsai)
:::

1.  Place the [configuration operators](xref:configure) that corresponds to the hardware you intend
    to use between <xref:OpenEphys.Onix1.CreateContext> and <xref:OpenEphys.Onix1.StartAcquisition>.
    In this example, these are <xref:OpenEphys.Onix1.ConfigureBreakoutBoard> and
    <xref:OpenEphys.Onix1.ConfigureHeadstage64>.
1.  Confirm that the device that streams electrophysiology data is enabled. The
    [Rhd2164](https://intantech.com/products_RHD2000.html) device (an Intan ephys acquisition
    acquisition chip) on the headstage 64 is the only device used in this tutorial, so you can
    disable other devices on the headstage and on the breakout board.

## Stream Ephys Data into Bonsai

Place the relevant operators to stream electrophysiology data from your headstage:

::: workflow
![/workflows/tutorials/ephys-process-listen/ephys-data.bonsai workflow](../../workflows/tutorials/ephys-process-listen/ephys-data.bonsai)
:::

1.  We placed the <xref:OpenEphys.Onix1.Rhd2164Data> place into the workflow because the device on
    headstage 64 that streams electrophysiology data is the Rhd2164 Intan amplifier. 
1.  Select the relevant member from the data frames that `Rhd2164Data` produces. In this example, the
    relevant member is AmplifierData. To do this, right-click `Rhd2164Data`, hover over the
    output option in the context menu, and select "AmplifierData" from the list.

Visualize the raw data to confirm that the ephys data operator is streaming data. 

## Detect Spikes

### Select and reorder channels

Connect a <xref:Bonsai.Dsp.SelectChannels> operator to the electrophysiology data stream and edit its "Channels" property:

::: workflow
![/workflows/tutorials/ephys-process-listen/spike_select-channels.bonsai workflow](../../workflows/tutorials/ephys-process-listen/spike_select-channels.bonsai)
:::

- Remember indexing starts at 0.
- Reorder channels by listing the channel numbers in the order in which you want to visualize the
  channels.
<!-- - Use commas to list multiple channels and brackets for ranges. -->

### Center the signal around zero

Connect a <xref:Bonsai.Dsp.ConvertScale> operator to the `SelectChannels` operator and set its properties:

::: workflow
![/workflows/tutorials/ephys-process-listen/spike_center-data.bonsai workflow](../../workflows/tutorials/ephys-process-listen/spike_center-data.bonsai)
:::

- Edit its Shift property to subtract 2^bit depth - 1^ from the signal. In this example, we shift
  -32768 because the Rhd2164 device outputs unsigned 16-bit data.
- Set the Depth property to S16 or F32. A sufficiently large data type is required to represent
  ephys data without overflow.

### Scale the signal to microvolts

Connect a second `ConvertScale` to the first `ConvertScale` and set its properties:

::: workflow
![/workflows/tutorials/ephys-process-listen/spike_scale-data.bonsai workflow](../../workflows/tutorials/ephys-process-listen/spike_scale-data.bonsai)
:::

- Edit its Scale property to multiply the signal by a scalar in order to get microvolt values. This
  scalar is determined by the gain of the amplifier and resolution the ADC contained in the bioacquisition
  device. In this example, we scale by 0.195 because the Rhd2164 device on headstage64 has a step size
  of 0.195&nbsp;μV/bit. 
- Set the Depth property at F32 which is required to represent decimal values. 

Visualize the transformed data to confirm the output of the shifting and scaling operations are
performed as expected, i.e. that the signal is centered around zero and that the values make sense
in microvolts.

> [!NOTE]
> Although both the shift and scale computations can be done with a single `ConvertScale`, the
> calculation is more straightforward using two operators connected in series because `ConvertScale`
> applies the "shift" transformation after applying the "scale" transformation. If we used a single
> operator, we would have to pre-scale the Shift property.

### Apply a filter

Connect a `FrequencyFilter` operator to the second `ConvertScale` operator and set its properties:

::: workflow
![/workflows/tutorials/ephys-process-listen/spike_filter-data.bonsai workflow](../../workflows/tutorials/ephys-process-listen/spike_filter-data.bonsai)
:::

- Set its SampleRate property to 30000. Ephys data in all devices is 30 kHz.
- Set the FilterType property to an adequate type. In this example, we use a band pass filter to
  look at spikes and remove slowly changing signals.
- Set the Cutoff1 and Cutoff2 properties to adequate values. 

Visualize the filtered data to confirm that it matches your expectations.

> [!TIP] 
> If you choose to save data, we recommend you place the `MatrixWriter` operator before filtering
> and scaling to save raw data instead of scaled or filtered data. Converting to microvolts with the
> second `ConvertScale` operator increases the size of your data (because it's converted to F32 from
> S16) without increasing meaningful information. Filtering with the `FrequencyFilter` operator
> before recording removes signal in irrecoverable ways. It's preferable to either save both or apply
> another filter when loading and processing the data. 

### Detect spikes with fixed threshold

::: workflow
![/workflows/tutorials/ephys-process-listen/spike_detect.bonsai workflow](../../workflows/tutorials/ephys-process-listen/spike_detect.bonsai)
:::

Based on the amplitude of the signal on the selected channel, set a fixed threshold for detecting
spikes. <!-- discuss these details? -->

Visualize the spike data.

## Listen to Ephys

The output of `AmplifierData` can be directed into two separate signal processing streams. In other
words, it is possible for two downstream operators to receive the same sequence of
`AmplifierDataFrames`. This is helpful for creating two distinct disparate processes for the same
data stream, one for visualizing spikes in several channels as we did above and one for listening to a single channel as follows.

### Select a channel and process the signal for audio

::: workflow
![/workflows/tutorials/ephys-process-listen/audio_process.bonsai workflow](../../workflows/tutorials/ephys-process-listen/audio_process.bonsai)
:::

The same basic steps as the [Spike Detection](xref:ephys-process-listen#detect-spikes) section are performed.
However, the property settings are critically different. 

- Select a single channel for listening instead of multiple channels for detecting spikes.
- Use the second `ConvertScale` to scale the signal by a value between 0 and 1 to control the volume
  of the audio signal instead of scaling by 0.195 to convert to microvolts. This `ConvertScale`
  effectively serves as a volume knob.

Visualize the data and compare it at various points in the processing pipeline to confirm it matches
your expectations.

### Play ephys data as audio

::: workflow
![/workflows/tutorials/ephys-process-listen/ephys-process-listen.bonsai workflow](../../workflows/tutorials/ephys-process-listen/ephys-process-listen.bonsai)
:::

Connect an `AudioPlayback` operator to `FrequencyFilter` and set its SampleRate property to 30000.

Providing data to `AudioPlayback` that is outside of the bounds of a signed 16&nbsp;bit integer
(-32,768 to +32,767) introduces clipping distortion into the audio signal, so it is recommended to
maintain a Scale property value of less than 1 for the volume knob `ConvertScale`. Maximize other
volume settings on your PC before exceeding 1.

<!-- 
## Refactoring the Workflow for your purpose

If the processing branches have overlap, it is possible to consolidate them. For example, if your
filter parameters and offset parameters are identical, this workflow behaves identically as the
example provided at the top of this page.

> [!TIP] 
> You can test the spike detection using pre-recorded data known to have spikes: recreate the
> workflow from this example in a new file without the hardware configuration chain and replace
> the ephys data-producing operators (in the case of the headstage64, replace the `Rhd2164` and
> `MemberSelector` operators) with a `MatrixReader` that reads from a file containing spiking
> ephys data in unsigned 16-bit format.

add this workflow and some sample data -->
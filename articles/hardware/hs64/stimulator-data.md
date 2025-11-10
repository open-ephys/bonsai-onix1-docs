---
uid: hs64_stimulator-data
title: Headstage 64 Stimulator Data
---

The following excerpt from the Headstage 64 [example
workflow](xref:hs64_workflow) demonstrates how to save the waveform parameters
and the hardware timestamp of every stimulus delivered as described in the
<xref:hs64_estim>, <xref:hs64_ostim>, and <xref:hs64_gpo-trigger> articles.

::: workflow
![/workflows/hardware/hs64/stimulator-data.bonsai workflow](../../../workflows/hardware/hs64/stimulator-data.bonsai)
:::

The <xref:OpenEphys.Onix1.Headstage64ElectricalStimulatorData> operator
generates a sequence of
[Headstage64ElectricalStimulatorDataFrames](xref:OpenEphys.Onix1.Headstage64ElectricalStimulatorDataFrame)
which contain data about when an electrical stimulus was delivered and the
corresponding electrical stimulation waveform. A frame is emitted when an
electrical stimulus is delivered. In the Headstage 64 example workflow, the
`Headstage64ElectricalStimulatorData`'s `DeviceName` property is set to
"Headstage64/Headstage64ElectricalStimulator". This links the
`Headstage64ElectricalStimulatorData` operator to the corresponding
configuration operator. Frames from this operators are saved to a file named
`estim_<filecount>.csv` using a <xref:Bonsai.IO.CsvWriter>.

The <xref:OpenEphys.Onix1.Headstage64OpticalStimulatorData> operator generates a
sequence of
[Headstage64OpticalStimulatorDataFrames](xref:OpenEphys.Onix1.Headstage64OpticalStimulatorDataFrame)
which contain data about when an optical stimulus was delivered and the
corresponding optical stimulation waveform. A frame is emitted when an optical
stimulus is delivered. In the Headstage 64 example workflow, the
`Headstage64OpticalStimulatorData`'s `DeviceName` property is set to
"Headstage64/Headstage64OpticalStimulator". This links the
`Headstage64OpticalStimulatorData` operator to the corresponding configuration
operator. Frames from this operators are saved to a file named `ostim_<filecount>.csv`
using a `CsvWriter`.


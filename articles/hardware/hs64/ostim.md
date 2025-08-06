---
uid: hs64_ostim
title: Headstage 64 Optical Stimulation
---

The following excerpt from the Headstage64 [example workflow](xref:hs64_workflow) demonstrates optical stimulation by
triggering a train of pulses following a press of the ◯ key on the breakout board.

::: workflow
![/workflows/hardware/hs64/ostim.bonsai workflow](../../../workflows/hardware/hs64/ostim.bonsai)
:::

The <xref:OpenEphys.Onix1.DigitalInput> operator generates a sequence of
[DigitalInputDataFrames](xref:OpenEphys.Onix1.DigitalInputDataFrame). Although the digital inputs
are sampled at 4 Mhz, these data frames are only emitted when the port status changes (i.e., when a
pin, button, or switch is toggled). In the Breakout Board example workflow, the `DigitalInput`'s
`DeviceName` property is set to "BreakoutBoard/DigitalInput". This links the `DigitalInput` operator
to the corresponding configuration operator. 

<xref:OpenEphys.Onix1.BreakoutButtonState> is selected from the `DigitalInputDataFrame`. It is an enumerator with values
that correspond to bit positions of the breakout board's digital port. When this type is connected to a `HasFlags`
operator, the enumerated values appear in the `HasFlags`'s `Value` property's dropdown menu. Because `HasFlags`'s
`Value` is set to "Circle", its output is "True" when the selected `BreakoutButtonState` bit field contains the
"Circle" flag.

When the <xref:OpenEphys.Onix1.Headstage64OpticalStimulatorTrigger> operator receives a "True" value in its input
sequence, a stimulus waveform is triggered. The waveform can be modified by editing the
`Headstage64OpticalStimulatorTrig` operator's properties.
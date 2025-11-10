---
uid: hs64_gpo-trigger
title: Headstage 64 GPO Trigger
---

The following excerpt from the Headstage 64 [example
workflow](xref:hs64_workflow) demonstrates triggering a stimulus following a
press of the X key on the breakout board. The GPO trigger toggles a pin on the
headstage to trigger stimulus which occurs more instantaneously than writing to
a register on the headstage which is how the
<xref:OpenEphys.Onix1.Headstage64ElectricalStimulatorTrigger> and
<xref:OpenEphys.Onix1.Headstage64OpticalStimulatorTrigger> operators trigger
stimuli.

> [!NOTE]
> Only one (electrical or optical) stimulator can armed at a time. If both
> stimulators are armed, the electrical stimulator takes precedence, e.g.
> the electrical stimulator stays armed and the optical stimulator is
> automatically disarmed by the headstage firmware. If you want to interleave
> optical stimulation and electrical stimulation, you must coordinate the
> stimulators to be dynamically armed and disarmed.

::: workflow
![/workflows/hardware/hs64/gpo-trigger.bonsai workflow](../../../workflows/hardware/hs64/gpo-trigger.bonsai)
:::

The <xref:OpenEphys.Onix1.DigitalInput> operator generates a sequence of
[DigitalInputDataFrames](xref:OpenEphys.Onix1.DigitalInputDataFrame). Although
the digital inputs are sampled at 4 Mhz, these data frames are only emitted when
the port status changes (i.e., when a pin, button, or switch is toggled) when
`DigitalInput`'s `SampleRate` property is left blank such as is done in the
example workflow. The `DigitalInput`'s `DeviceName` property is set to
"BreakoutBoard/DigitalInput". This links the `DigitalInput` operator to the
corresponding configuration operator. 

[Buttons](xref:OpenEphys.Onix1.BreakoutButtonState) is selected from the
`DigitalInputDataFrame` and passed to a `HasFlags` operator, which filters the
sequence based on which button is pressed using the `Value` property's dropdown
menu. In this case, `HasFlags`'s `Value` is set to "Square", so its output is
"True" when an item its input sequence contains a "Square" flag. The
<xref:Bonsai.Reactive.DistinctUntilChanged> operator only passes an item in its
input sequence if it's different from the previous item in the input sequence.
When the <xref:OpenEphys.Onix1.Headstage64GpoTrigger> operator receives a "True"
value in its input sequence, a stimulus waveform is triggered.
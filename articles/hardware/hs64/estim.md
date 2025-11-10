---
uid: hs64_estim
title: Headstage 64 Electrical Stimulation
---

The following excerpt from the Headstage 64 [example
workflow](xref:hs64_workflow) demonstrates electrical stimulation by triggering
a train of pulses following a press of the △ key on the breakout board.

> [!NOTE]
> Only one (electrical or optical) stimulator can armed at a time. If both
> stimulators are armed, the electrical stimulator takes precedence, e.g.
> the electrical stimulator stays armed and the optical stimulator is
> automatically disarmed by the headstage firmware. If you want to interleave
> optical stimulation and electrical stimulation, you must coordinate the
> stimulators to be dynamically armed and disarmed.

::: workflow
![/workflows/hardware/hs64/estim.bonsai workflow](../../../workflows/hardware/hs64/estim.bonsai)
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
menu. In this case, `HasFlags`'s `Value` is set to "Triangle", so its output is
"True" when an item its input sequence contains a "Triangle" flag. The
<xref:Bonsai.Reactive.DistinctUntilChanged> operator only passes an item in its
input sequence if it's different from the previous item in the input sequence.
The <xref:Bonsai.Reactive.Condition> operator only passes an item in its input
sequence if `Condition`'s internal logic is "True". In this case, `Condition`
has no internal logic (which can be inspected by selecting the node and pressing
<kbd>Ctrl+Enter</kbd>), so it uses the value of the Boolean in its input
sequence to decide whether or not to pass through an item in its input sequence
to its output sequence. 

The <xref:Bonsai.Expressions.DoubleProperty> operator emits a
<xref:System.Double> determined by `Double`'s `Value` property whenever it
receives an item in its input sequence. Each double in the input sequence
received by <xref:OpenEphys.Onix1.Headstage64ElectricalStimulatorTrigger>
triggers an electrical stimulus waveform. The value of the double determines the
delay in microseconds, executed on the hardware, between triggering the stimulus
and delivery of the stimulus. When `Double`'s `Value` property is set to zero,
there is no delay.
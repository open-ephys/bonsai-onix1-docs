---
uid: hs64_estim
title: Headstage 64 Electrical Stimulation
---

The following excerpt from the Headstage 64 [example
workflow](xref:hs64_workflow) demonstrates electrical stimulation by triggering
a train of pulses following a press of the △ key on the breakout board.

::: workflow
![/workflows/hardware/hs64/estim.bonsai workflow](../../../workflows/hardware/hs64/estim.bonsai)
:::

The <xref:OpenEphys.Onix1.DigitalInput> operator generates a sequence of
[DigitalInputDataFrames](xref:OpenEphys.Onix1.DigitalInputDataFrame). Although
the digital inputs are sampled at 4 Mhz, these data frames are only emitted when
the port status changes (i.e., when a pin, button, or switch is toggled). In the
Headstage 64 example workflow, the `DigitalInput`'s `DeviceName` property is
set to "BreakoutBoard/DigitalInput". This links the `DigitalInput` operator to
the corresponding configuration operator. 

<xref:OpenEphys.Onix1.BreakoutButtonState> is selected from the
`DigitalInputDataFrame`. It is an enumerator with values that correspond to bit
positions of the breakout board's digital port. When this type is connected to a
`HasFlags` operator, the enumerated values appear in the `HasFlags`'s `Value`
property's dropdown menu. Because `HasFlags`'s `Value` is set to "Triangle", its
output is "True" when the selected `BreakoutButtonState` bit field contains the
"Triangle" flag. The <xref:Bonsai.Reactive.DistinctUntilChanged> operator only
allows passes an item in its input sequence if it's different from the previous
item in the input sequence. The <xref:Bonsai.Reactive.Condition> operator only
passes an item in its input sequence if `Condition`'s internal logic is "True".
In this case, `Condition` has no internal logic (which can be inspected by
selecting the node and pressing <kbd>Ctrl+Enter</kbd>), so it uses the value of
the Boolean in its input sequence to decide whether or not to pass a value. The
<xref:Bonsai.Expressions.DoubleProperty> operator emits a value determined by
its `Value` property whenever it receives an item in its input sequence. T This
value is used to determine the delay between triggering the stimulus and
delivery of the stimulus. When `Double`'s `Value` property is set to zero, there
is no such delay.

When the <xref:OpenEphys.Onix1.Headstage64ElectricalStimulatorTrigger> operator
receives a "True" value in its input sequence, a stimulus waveform is triggered.
The waveform can be modified by editing the
`Headstage64ElectricalStimulatorTrig` operator's properties.
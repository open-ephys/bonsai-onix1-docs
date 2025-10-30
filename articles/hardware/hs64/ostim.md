---
uid: hs64_ostim
title: Headstage 64 Optical Stimulation
---

The following excerpt from the Headstage64 [example
workflow](xref:hs64_workflow) demonstrates optical stimulation by triggering a
train of pulses following a press of the ◯ key on the breakout board.

::: workflow
![/workflows/hardware/hs64/ostim.bonsai workflow](../../../workflows/hardware/hs64/ostim.bonsai)
:::

[!INCLUDE [<digital-io-info>](<../../../includes/breakout-digital-io.md>)]

<xref:OpenEphys.Onix1.BreakoutButtonState> is selected from the
`DigitalInputDataFrame`. It is an enumerator with values that correspond to bit
positions of the breakout board's digital port. When this type is connected to a
`HasFlags` operator, the enumerated values appear in the `HasFlags`'s `Value`
property's dropdown menu. Because `HasFlags`'s `Value` is set to "Circle", its
output is "True" when the selected `BreakoutButtonState` bit field contains the
"Circle" flag. The <xref:Bonsai.Reactive.DistinctUntilChanged> operator only
allows passes an item in its input sequence if it's different from the previous
item in the input sequence. The <xref:Bonsai.Reactive.Condition> operator only
passes an item in its input sequence if `Condition`'s internal logic is "True".
In this case, `Condition` has no internal logic (which can be inspected by
selecting the node and pressing <kbd>Ctrl+Enter</kbd>), so it uses the value of
the Boolean in its input sequence to decide whether or not to pass a value. The
<xref:Bonsai.Expressions.DoubleProperty> operator emits a value determined by
its `Value` property whenever it receives an item in its input sequence. This
value is used to determine the delay between triggering the stimulus and
delivery of the stimulus. When `Double`'s `Value` property is set to zero, there
is no such delay.

When the <xref:OpenEphys.Onix1.Headstage64OpticalStimulatorTrigger> operator
receives a "True" value in its input sequence, a stimulus waveform is triggered.
The waveform can be modified by editing the `Headstage64OpticalStimulatorTrig`
operator's properties.
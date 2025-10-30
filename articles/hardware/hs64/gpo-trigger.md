---
uid: hs64_gpo-trigger
title: Headstage 64 GPO Trigger
---

The following excerpt from the Headstage 64 [example
workflow](xref:hs64_workflow) demonstrates triggering a stimulus following a
press of the X key on the breakout board. The GPO trigger uses a pin on the
headstage to trigger stimulus more instantaneously than other trigger methods
that write to a register on the hardware which takes more time. However, this
trigger operator does not provide stimulus feedback as discussed in
<xref:hs64_stimulator-data> nor is it capable of distinguishing between applying
optical or electrical stimulus. If you want to use the GPO trigger to only
trigger electrical stimulus, the electrical stimulator should be the only
stimulator device armed on the headstage. If you want to use the GPO trigger to
only trigger optical stimulus, the optical stimulator should be the only
stimulator device armed on the headstage. 

::: workflow
![/workflows/hardware/hs64/gpo-trigger.bonsai workflow](../../../workflows/hardware/hs64/gpo-trigger.bonsai)
:::

The <xref:OpenEphys.Onix1.DigitalInput> operator generates a sequence of
[DigitalInputDataFrames](xref:OpenEphys.Onix1.DigitalInputDataFrame). Although
the digital inputs are sampled at 4 Mhz, these data frames are only emitted when
the port status changes (i.e., when a pin, button, or switch is toggled). In the
Breakout Board example workflow, the `DigitalInput`'s `DeviceName` property is
set to "BreakoutBoard/DigitalInput". This links the `DigitalInput` operator to
the corresponding configuration operator. 

<xref:OpenEphys.Onix1.BreakoutButtonState> is selected from the
`DigitalInputDataFrame`. It is an enumerator with values that correspond to bit
positions of the breakout board's digital port. When this type is connected to a
`HasFlags` operator, the enumerated values appear in the `HasFlags`'s `Value`
property's dropdown menu. Because `HasFlags`'s `Value` is set to "Square", its
output is "True" when the selected `BreakoutButtonState` bit field contains the
"Square" flag. The <xref:Bonsai.Reactive.DistinctUntilChanged> operator only
allows passes an item in its input sequence if it's different from the previous
item in the input sequence. The <xref:Bonsai.Reactive.Condition> operator only
passes an item in its input sequence if `Condition`'s internal logic
is "True". In this case, `Condition` has no internal logic (which can
be inspected by selecting the node and pressing <kbd>Ctrl+Enter</kbd>), so it
uses the value of the Boolean in its input sequence to decide whether or not to
pass a value.

When the <xref:OpenEphys.Onix1.Headstage64ElectricalStimulatorTrigger> operator
receives a "True" value in its input sequence, a stimulus waveform is triggered.
The waveform can be modified by editing the
`Headstage64ElectricalStimulatorTrig` operator's properties.
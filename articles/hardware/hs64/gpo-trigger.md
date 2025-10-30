---
uid: hs64_gpo-trigger
title: Headstage 64 GPO Trigger
---

The following excerpt from the Headstage 64 [example
workflow](xref:hs64_workflow) demonstrates triggering a stimulus following a
press of the X key on the breakout board. The GPO trigger toggles a pin on the
headstage to trigger stimulus more instantaneously than writing to a register
which is how other Headstage 64 operators trigger stimulus.

> [!NOTE]
> If you want to use the GPO trigger to only trigger electrical stimulus, the
> electrical stimulator should be the only stimulator device armed on the
> headstage. If you want to use the GPO trigger to only trigger optical
> stimulus, the optical stimulator should be the only stimulator device armed on
> the headstage. 

::: workflow
![/workflows/hardware/hs64/gpo-trigger.bonsai workflow](../../../workflows/hardware/hs64/gpo-trigger.bonsai)
:::

[!INCLUDE [<digital-io-info>](<../../../includes/breakout-digital-io.md>)]

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
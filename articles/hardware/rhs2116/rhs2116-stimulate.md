---
uid: rhs2116_stimulate
title: Rhs2116 Stimulating
---

The following excerpt from the HeadstageRhs2116 [example workflow](xref:rhs2116) demonstrates the Rhs2116
stimulation functionality by using button presses on the breakout board to trigger multichannel stimulation sequences on the headstage.

::: workflow
![/workflows/hardware/rhs2116/rhs2116-stimulate.bonsai workflow](../../../workflows/hardware/rhs2116/rhs2116-stimulate.bonsai)
:::

The <xref:OpenEphys.Onix1.DigitalInput> operator generates a sequence of
[DigitalInputDataFrames](xref:OpenEphys.Onix1.DigitalInputDataFrame). Although the digital inputs
are sampled at 4 Mhz, these data frames are only emitted when the port status changes (i.e., when a
pin, button, or switch is toggled). In the example workflow, the `DigitalInput`'s DeviceName
property is set to "BreakoutBoard/DigitalInput". This links the `DigitalInput` operator to the
Breakout Board's digital inputs. 

<xref:OpenEphys.Onix1.BreakoutButtonState> is selected from the `DigitalInputDataFrame`. It is an
enumerator with values that correspond to bit positions of the breakout board's digital port.
`Buttons` connects to `Condition` which is inspectable with the <kbd>F12</kbd> hotkey. `Condition`
contains a `HasFlags` operator. Because `HasFlags`'s Value property is set to "Triangle", it outputs
"True" when the △ button is pressed. `Condition` passes `BreakoutButtonState` to `Double`
when its internal conditional statement evaluates to true. `Double` emits a value of type
<xref:System.Double> to <xref:OpenEphys.Onix1.Rhs2116StimulusTrigger> anytime it receives an item in
its upstream sequence. 

When `Rhs2116StimulusTrigger` receives a double from the upstream sequence, a stimulus is triggered.
The value of the double determines the duration of a precise hardware delay between triggering and
actually delivering the stimulus in microseconds. If the double is zero, there is no hardware delay and the stimulus sequence is started as soon as the trigger is received. The stimulus
waveform delivered is configured in the [Headstage RHS2116 GUI](xref:rhs2116_gui). If the sequencer
is busy or the stimulator is disarmed when the trigger occurs, stimulus won't be delivered. This can
be checked using the <xref:OpenEphys.Onix1.Rhs2116TriggerData> operator as demonstrated in the
<xref:rhs2116_trigger_data> page.

`Rhs2116StimulusTrigger`'s DeviceName property is set to "HeadstageRhs2116/StimulusTrigger" to link
this operator to the Rhs2116 devices on the Headstage Rhs2116. 

> [!TIP] 
> For more details about configuring the Rhs2116 and its stimulation capabilities, read the
> [datasheet](https://intantech.com/files/Intan_RHS2116_datasheet.pdf). 
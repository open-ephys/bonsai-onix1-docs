---
uid: rhs2116_stimulate
title: Rhs2116 Stimulating
---

The following excerpt from the HeadstageRhs2116 [example workflow](xref:rhs2116) demonstrates the Rhs2116
stimulation functionality by streaming and saving data from the Rhs2116 device.

::: workflow
![/workflows/hardware/rhs2116/rhs2116-stimulate.bonsai workflow](../../../workflows/hardware/rhs2116/rhs2116-stimulate.bonsai)
:::

The <xref:OpenEphys.Onix1.DigitalInput> operator generates a sequence of
<xref:OpenEphys.Onix1.DigitalInputDataFrame>s. Although the digital inputs are sampled at 4 Mhz,
these data frames are only emitted when the port status changes (i.e., when a pin, button, or switch
is toggled). In the example workflow, the `DigitalInput`'s DeviceName property is
set to "BreakoutBoard/DigitalInput". This links the `DigitalInput` operator to the Breakout Board's
digital inputs. 

<xref:OpenEphys.Onix1.BreakoutButtonState> is selected from the `DigitalInputDataFrame`. It is an
enumerator with values that correspond to bit positions of the breakout board's digital port.
`Buttons` connects to `Condition` which is inspectable with the <kbd>F12</kbd> hotkey. `Condition`
contains a `HasFlags` operator. Because `HasFlags`'s Value property is set to "Triangle", it outputs
"True" when the △ button is pressed. `Condition` passes `BreakoutButtonState` to `Double`
when the its internal conditional statement is evaluated is true. `Double` emits a value of type
<xref:System.Double> to <xref:OpenEphys.Onix1.Rhs2116StimulusTrigger> anytime it receives an item in
its upstream sequence. 

When `Rhs2116StimulusTrigger` receives a double from the upstream sequence, a stimulus waveform is
triggered. Its DeviceName property is set to "HeadstageRhs2116/StimulusTrigger" to link this
operator to the Rhs2116s on the Headstage Rhs2116. [Open the Headstage RHS2116
GUI](xref:rhs2116_gui) to edit the stimulus waveform.

> [!TIP] 
> For more details about configuring the Rhs2116 and its stimulation capabilities, read the
> [datasheet](https://intantech.com/files/Intan_RHS2116_datasheet.pdf). 
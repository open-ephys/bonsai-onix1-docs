---
uid: breakout_digital-inputs
title: Breakout Board Digital Inputs
hardware: true
device: digital inputs
videoCaption: This visualizes digital input data using Bonsai visualizers. The "Buttons" window shows which buttons are being pressed. The "HasFlags" window shows whether or not certain button are being pressed (in the case of the breakout board example workflow, "Triangle" or "X"). These visualizers correspond to actual button presses which are demonstrated by the bottom-right breakout board inset.
---

The following excerpt from the Breakout Board [example workflow](xref:breakout_workflow) demonstrates digital inputs
functionality by responding to button presses and saves digital inputs data.

::: workflow
![/workflows/hardware/breakout/digital-inputs.bonsai workflow](../../../workflows/hardware/breakout/digital-inputs.bonsai)
:::

The <xref:OpenEphys.Onix1.DigitalInput> operator generates a sequence of <xref:OpenEphys.Onix1.DigitalInputDataFrame>s.
Although the digital inputs are sampled at 4 Mhz, these data frames are only emitted when the port status changes (i.e.,
when a pin, button, or switch is toggled). The digital input ports on the Breakout Board operate at a 3.3V logic levels
but are also 5V tolerant. In the Breakout Board example workflow, the `DigitalInput`'s `DeviceName` property is set to
"BreakoutBoard/DigitalInput". This links the `DigitalInput` operator to the corresponding configuration operator. 

The [CsvWriter](xref:Bonsai.IO.CsvWriter) operator writes the `Clock`, `DigitalInputs`, and `Buttons` members from the
`DigitalInputDataFrame` to a file with the following name format: `digital-input_<filecount>.csv`. Because `CsvWriter`
is a _sink_ operator, its output sequence is equivalent to its input sequence. In other words, its output is equivalent
to `DigitalInput`'s output. Therefore, it's possible to use
[MemberSelector](xref:Bonsai.Expressions.MemberSelectorBuilder) operators on the `CsvWriter` to select members from
`DigitalInputDataFrame`. This is most easily performed by clicking the relevant members that appear by hovering over the
"Output" option that appears in the context menu that appears after right-clicking the `CsvWriter` node. The members
selected in the workflow, <xref:OpenEphys.Onix1.DigitalPortState> and <xref:OpenEphys.Onix1.BreakoutButtonState>, are
enumerators with values that correspond to bit positions of the breakout board's digital ports. When `DigitalPortState`
or `OpenEphys.Onix1.BreakoutButtonState` is connected to a `HasFlags` operator, the names that appear in the
`HasFlags`'s `Value` property's dropdown menu correspond to bit positions in the respective digital input port. In this
workflow, the top `HasFlags` operator checks if `Triangle` or `X` are `True`. 
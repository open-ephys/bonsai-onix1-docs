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

`Clock`, `DigitalInputs`, and `Buttons` are all members of `DigitalInputDataFrame` which are each
selected by a [MemberSelector](xref:Bonsai.Expressions.MemberSelectorBuilder) operator. They contain
the <xref:OpenEphys.Onix1.ContextTask.AcquisitionClockHz>-based sample times, digital port status,
and buttons' status, respectively. The [MatrixWriter](xref:Bonsai.Dsp.MatrixWriter) operators save
the selected members to files with the following format: `digital-clock_<filecount>.raw`,  and
`digital-pins_<filecount>.raw`, and `digital-buttons_<filecount>.raw`, respectively. 

Because `MatrixWriter` is a _sink_ operator, its output sequence is equivalent to its input
sequence. For example, the output of the `MatrixWriter` connected to `Button` is equivalent to
`Button`'s output. Therefore, it's possible to process digital data by branching directly off the
`MatrixWriter` operators. The selected `DigitalInputs` and `Buttons` members are both enumerator
types: <xref:OpenEphys.Onix1.DigitalPortState> and <xref:OpenEphys.Onix1.BreakoutButtonState>,
respectively. Enumerators assign names to values. When `DigitalPortState` or `BreakoutButtonState`
is connected to a `HasFlags` operator, these names appear in the `HasFlags`'s `Value` property's
dropdown menu. In this case, the values that these names represent correspond to bit positions of
the breakout board's digital ports. In this workflow, the top `HasFlags` operator checks if `Pin0`
is `True`, and the bottom `HasFlags` operator checks if `Triangle` or `X` are `True`.
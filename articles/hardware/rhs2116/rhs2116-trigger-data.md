---
uid: rhs2116_trigger_data
title: Rhs2116 Trigger Data
---

The following excerpt from the HeadstageRhs2116 [example workflow](xref:rhs2116) demonstrates how to
save data about the Rhs2116 stimulus.

::: workflow 
![/workflows/hardware/rhs2116/rhs2116-trigger-data.bonsai workflow](../../../workflows/hardware/rhs2116/rhs2116-trigger-data.bonsai) 
:::

The <xref: OpenEphys.Onix1.Rhs2116TriggerData> operator generates a sequence of 
[Rhs2116TriggerDataFrames](xref:OpenEphys.Onix1.Rhs2116TriggerDataFrame). Its DeviceName property is set to
"HeadstageRhs2116/StimulusTrigger" which links `Rhs2116TriggerData` to the stimulus devices on the
RHS2116 Headstage.

The <xref: Bonsai.IO.CsvWriter> operator selects Clock, Delay, Status, and Origin members from the
`Rhs2116TriggerDataFrame` to write to a file with a name of the following format:
`rhs2116trigger_<filecount>.csv`. These members are selected using the `CsvWriter`'s `Selector`
property. They contain the following information:
- **Clock**: the <xref:OpenEphys.Onix1.ContextTask.AcquisitionClockHz>-based sample times that a
  stimulus trigger is received
- **Delay**: the delay between receiving the trigger to the physical application of the stimulus, in
  microseconds, as defined by the input to <xref: OpenEphys.Onix1.Rhs2116StimulusTrigger>
- **Status**: the delivery status of the stimulus. This includes whether the stimulus was delivered
  or why it might not have been delivered (i.e. if stimulator is disarmed or the stimulus sequencer
  is already in the midst of delivering a stimulus).
- **Origin**: specifies whether the stimulus was triggered by writing to a register, setting a local
  GPIO pin, or via an external synchronization source
  
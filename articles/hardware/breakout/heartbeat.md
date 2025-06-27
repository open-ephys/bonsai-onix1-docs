---
uid: breakout_heartbeat
title: Breakout Board Heartbeat
hardware: true
device: heartbeat
---

ONIX has a single special device, called a heartbeat, that produces data at
regular intervals and is always enabled. When data is read from the hardware by
software, the reading thread will block until enough data has been produced by
the hardware. If no devices are enabled, the software would block forever. The
heartbeat prevents this from happening since it is always enabled and always
producing data. In practice, you can ignore the heartbeat functionality. In any
case, the following excerpt from the Breakout Board [example
workflow](xref:breakout_workflow) demonstrates how to observe the heartbeat.

::: workflow
![/workflows/hardware/breakout/heartbeat.bonsai workflow](../../../workflows/hardware/breakout/heartbeat.bonsai)
:::

The <xref:OpenEphys.Onix1.HeartbeatData> operator generates a sequence of
[HeartbeatDataFrames](xref:OpenEphys.Onix1.HeartbeatDataFrame). `HeartbeatData`
emits `HeartbeatDataFrames` at a regular interval defined during
<xref:breakout_configuration> using the
<xref:OpenEphys.Onix1.ConfigureBreakoutBoard>'s `Heartbeat BeatsPerSecond`
property (in our case 100 Hz, which is the minimum allowable frequency). The
`HeartbeatData`'s `DeviceName` property is set to "BreakoutBoard/Heartbeat".
This links the `HeartbeatData` operator to the corresponding configuration
operator. The [MemberSelector](xref:Bonsai.Expressions.MemberSelectorBuilder)
operator selects the `Clock` member from the `HeartbeatDataFrame` so the user
can visualize the number of clock cycles that have passed for a given heartbeat
pulse if they double-click the `Clock` node.
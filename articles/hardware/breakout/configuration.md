---
uid: breakout_configuration
title: Breakout Board Configuration
configuration: true
hardware: Breakout Board
operator: ConfigureBreakoutBoard
dataRate: 2.5
timeUntilFullBuffer: 800 μs
blockReadSize: 2048
workflowLocation: workflow
---

## Configuring the Breakout Board
The `ConfigureBreakoutBoard` operator groups the properties
for all the devices that the breakout board supports. Each device in the
property pane can be expanded to expose individual properties that govern their
behavior. 

> [!TIP] 
> The `Properties` section of the <xref:OpenEphys.Onix1.ConfigureBreakoutBoard>
> operator provides documentation on the effect of all of the breakout board's
> configuration settings.

To examine and edit the breakout board's properties, click on the `Breakout
Board` node to select it. The properties pane will appear immediately right of
the workflow editor. Expanding each of the devices within the properties pane
provides access to their configuration settings. The following video
demonstrates how properties were edited for the example workflow:

<figure>
  <video width="100%" loop="true" controls="true"><source src="../../../images/hardware/breakout/configuration.mp4" type="video/mp4"/></video>
  <figcaption>
    This video shows how the breakout board's properties are changed in Bonsai.
    Specifically, the <code>AnalogIO Direction0</code> property is set to
    "Output", and the <code>MemoryMonitor Enable</code> property is set to
    "True". It's not necessary to repeat those steps if the workflow is
    copied/pasted into your editor because they are saved with the workflow.
  </figcaption>
</figure>

Namely, the following properties were changed form their default values in the
breakout board example workflow:

- The `BreakoutBoard`'s `AnalogIO Direction0` property is set to `Output`.
- The `BreakoutBoard`'s `MemoryMonitor Enable` property is set to `True`.
- The `BreakoutBoard`'s `OutputClock Gate` property is set to `True`.

[!INCLUDE [timestamp-info](../../../includes/configuration-timestamp.md)]
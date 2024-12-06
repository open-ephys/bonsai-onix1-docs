---
uid: hs64_configuration
title: Headstage64 Configuration
hardware: Headstage64
configuration: true
operator: ConfigureHeadstage64
dataRate: 4.1
timeUntilFullBuffer: 1000 μs
blockReadSize: 4096
workflowLocation: workflow
---

## Configuring the Breakout Board and Headstage64

The `ConfigureBreakoutBoard` operator configures the Onix Breakout Board. In the Headstage64 example tutorial, it is configured to enable digital inputs to serve as a trigger for the Headstage64's electrical and optical stimulation and to enable monitoring of the percentage of memory occupied. This is accomplished by leaving all of the `ConfigureBreakoutBoard` properties set to their default values except its `Memory Monitor` `Enable` property is set to `True`. 

The `ConfigureHeadstage64` operator is used to configure the Headstage64. In the Headstage64 example tutorial, it is configured to enable streaming of electrophysiology data from a Rhd2164 amplifier, orientation data from the on-board Bno055 IMU, and position data from the Ts4231. This is accomplished in the Headstage64 example workflow by leaving all of the `ConfigureHeadstage64` properties set to their default values.

[!INCLUDE [timestamp-info](../../../includes/configuration-timestamp.md)]
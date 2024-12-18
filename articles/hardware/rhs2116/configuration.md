---
uid: rhs2116_configuration
title: Headstage Rhs2116 Configuration
hardware: Headstage Rhs2116
configuration: true
operator: ConfigureHeadstageRhs2116
dataRate: 2.1
timeUntilFullBuffer: 1 ms
blockReadSize: 4096
workflowLocation: workflow
---

## Configuring the Breakout Board and Headstage Rhs2116

The `ConfigureBreakoutBoard` operator configures the Onix Breakout Board. In the Headstage Rhs2116 example tutorial, it is
configured to enable digital inputs to serve as a trigger for the Headstage Rhs2116's electrical and optical stimulation
and to enable monitoring of the percentage of memory occupied. This is accomplished by leaving all of the
`ConfigureBreakoutBoard` properties set to their default values except its `Memory Monitor` `Enable` property is set to
`True`. 

The `ConfigureHeadstageRhs2116` operator is used to configure the Headstage Rhs2116. In the Headstage Rhs2116 example
tutorial, it is configured to enable streaming of electrophysiology data from a Rhs2116 amplifier, orientation data from
the on-board Bno055 IMU, and position data from the Ts4231. This is accomplished in the Headstage Rhs2116 example
workflow by leaving all of the `ConfigureHeadstageRhs2116` properties set to their default values.

[!INCLUDE [timestamp-info](../../../includes/configuration-timestamp.md)]
---
uid: rhs2116_configuration
title: Headstage Rhs2116 Configuration
hardware: Headstage Rhs2116
configuration: true
operator: ConfigureHeadstageRhs2116
dataRate: 2.1
timeUntilFullBuffer: 1 ms
blockReadSize: 4096
workflowLocation: overview
---

## Configuring the Breakout Board and Headstage Rhs2116

The `ConfigureBreakoutBoard` operator configures the Onix Breakout Board. In the
Headstage Rhs2116 example tutorial, it is configured to enable digital inputs to
serve as a trigger for the Headstage Rhs2116's 32-channel electrical stimulator
and to enable monitoring of the percentage of hardware memory being used. All of
the `ConfigureBreakoutBoard` properties set to their default values except its
Memory Monitor Enable property is set to "True".

The `ConfigureHeadstageRhs2116` operator is used to configure the headstage. In
the Headstage Rhs2116 example tutorial, it is configured to enable streaming of
electrophysiology data from the headstage's dual Rhs2116 chips.

[!INCLUDE [timestamp-info](../../../includes/configuration-timestamp.md)]

> [!TIP]
> For additional details on how to configure the headstage, as well as how to
> set stimulus waveforms, check out the <xref:rhs2116_gui> page.
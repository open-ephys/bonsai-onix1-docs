---
uid: onix-acquisition
title: Data Acquisition
---

Data produced by ONIX hardware is captured using data input
operators and sent to hardware using data output operators, respectively. This
section covers their use.

## Acquire Data

Streaming data into Bonsai requires at least one [data I/O operator](xref:dataio).

### Set up data I/O operator(s)

Place a data I/O operator and set its DeviceName property for every device from which you would like
to stream. Setting the DeviceName property will tell the operator from which device to stream data.
This is referred to linking the data I/O operator to the device. Take this workflow for example:

::: workflow
![Workflow with data operator](../../workflows/getting-started/polled-bno055.bonsai)
:::

AnalogInput's DeviceName property is set to "BreakoutBoard/AnalogIO" so it will stream data from the
AnalogIO device on the breakout board.

## Use Multiple Instances of Identical Hardware

### Multiple headstages/miniscopes

Linking the data I/O operator to devices when using two identical headstages or
miniscopes involves an additional step: renaming a configuration operator.
Suppose you want to stream orientation data from two Neuropixels 2.0 Headstages
through using two <xref:OpenEphys.Onix1.PolledBno055Data> operators. By default,
the <xref:OpenEphys.Onix1.ConfigureHeadstageNeuropixelsV2e> operators are both
named "HeadstageNeuropixelsV2e". This causes their devices to also have
identical names, "HeadstageNeuropixelsV2e/PolledBno055". The two headstages and
their devices must be disambiguated. To do this, you must edit one or both of
headstages' `Name` property:

![Editing the name property of a configuration operator](../../images/edit-name-property.png){width=650px}

After this, the disambiguated source can be selected for each data operator

![Select a source for a Data operator](../../images/select-alternative-data-sources.png){width=650px}


In the following workflow workflow, the `Name` property of each
<xref:OpenEphys.Onix1.ConfigureHeadstageNeuropixelsV2e> has been changed from
"HeadstageNeuropixelsV2e" to "HS-NPX-AB" and "HS-NPX-B". The `DeviceName` of
each of the <xref:OpenEphys.Onix1.PolledBno055Data> operators has been set to
"HS-NPX-A/PolledBno055" and "HS-NPX-B/PolledBno055" from the dropdown so each
operator will take data from a different headstage.

::: workflow
![/workflows/polled-bno055-data-alias.bonsai workflow](../../workflows/getting-started/polled-bno055-data-alias.bonsai)
:::

### Multiple ONIX systems

If a second ONIX system is used on the same computer, a second configuration
chain operator is required. In this case, the `Index` property of the
configuration chain that corresponds to the second system should be set to 1. If
three systems are used, they would have `Index` values of 0, 1, and 2. etc.

::: workflow
![/workflows/getting-started/multiple-breakout.bonsai workflow](../../workflows/getting-started/multiple-breakout.bonsai)
:::

Now that you can stream data into Bonsai from ONIX hardware, the next step is
visualize the data.

## Minimum Version Check

If you start a workflow and are presented an exception such as this:

![Exception showing an attempt to acquire from device with unsupported gateware version](../../images/unsupported-version.png)

you must either update the gateware on your hardware or or revert to a software
that supports the indicated version of the gateware. 
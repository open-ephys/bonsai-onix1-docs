---
uid: property-categories
title: Property Categories
---

There are specific categories of properties that define when and how an operator's properties can be
modified. 

## Configuration & Acquisition Properties

<span class="badge oe-badge-border oe-badge-yellow" id="configuration">Configuration</span>
properties have an effect on hardware when a workflow is started and are used to initialize the
hardware state. Even if they are changed while a workflow is running, they will not have an effect
until the workflow is restarted.

<span class="badge oe-badge-border oe-badge-blue" id="acquisition">Acquisition</span> properties
have an immediate effect on hardware when the workflow is running. For instance, stimulus waveform
properties can be dynamically modified according to parameters in your workflow.

## Aggregate & Device Properties

<span class="badge oe-badge-border oe-badge-green" id="device-group">Device Group</span> properties are
only available through [device group configuration operators](xref:configure). 

<span class="badge oe-badge-border oe-badge-red" id="device">Device</span> properties are available
through [device configuration operators](xref:device-configure) and device group configuration
operators that derive them from device configuration operators. For example,
<xref:OpenEphys.Onix1.ConfigureHeadstage64> derives properties from
<xref:OpenEphys.Onix1.ConfigureBno055>. 

Writing <span class="badge oe-badge-border oe-badge-blue" id="acquisition">Acquisition</span> <span
class="badge oe-badge-border oe-badge-red" id="device">Device</span> properties to hardware
dynamically (e.g. while the the workflow is running) requires using device configuration operators
because externalizing device properties from a device group configuration operator in Bonsai is
currently not possible. 

<!-- <table style="border:transparent; width:20%">
  <tr>
    <td><span class="badge oe-badge-border oe-badge-orange">Configuration</span></td>
    <td><span class="badge oe-badge-border oe-badge-blue">Acquisition</span></td>
  </tr>
  <tr>
    <td><span class="badge oe-badge-border oe-badge-red">Device</span></td>
    <td><span class="badge oe-badge-border oe-badge-green">Device Group</span></td>
  </tr>
  <tr>
    <td><span class="badge oe-badge-border oe-badge-yellow">Fixed-rate</span></td>
    <td><span class="badge oe-badge-border oe-badge-purple">Variable-rate</span></td>
  </tr>
</table> -->
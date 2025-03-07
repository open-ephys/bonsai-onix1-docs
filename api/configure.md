---
uid: configure
title: Device Group Configuration Operators
---

Device Group configuration operators belong in a top-level configuration chain between
[CreateContext](xref:OpenEphys.Onix1.CreateContext) and
[StartAcquisition](xref:OpenEphys.Onix1.StartAcquisition) to configure ONIX hardware. These are
known as Device Group configuration operators because they configure a group of devices on a given
headstage, miniscope, breakout board, etc. Devices represent physical element
interfacing with the environment (e.g., an external sensor with a digital
communication interface like the BNO055, Neuropixels probes, or RHS2116 stimulus
trigger) or internal data sources (e.g., a controller based digital logic module
that generates system status reports like the port status controller).
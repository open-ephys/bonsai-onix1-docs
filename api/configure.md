---
uid: configure
title: Device Group Configuration Operators
---

Aggregate configuration operators belong in a top-level chain of operators between
[`CreateContext`](xref:OpenEphys.Onix1.CreateContext) and [`StartAcquisition`](xref:OpenEphys.Onix1.StartAcquisition) to
configure ONIX hardware hubs. These are known as device group configuration operators because they configure an aggregation
of devices (also referred to as a hardware hub) on a given headstage, miniscope, breakout board, etc..

Aggregate configuration operators are simply referred to as "Configuration Operators" in the
[Reference](xref:OpenEphys.Onix1) TOC for concision and simplicity as they are recommended starting-point operators for
configuring Open Ephys ONIX hardware. There are also <xref:device-configure>.
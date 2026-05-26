---
uid: configure
title: Configuration Operators
---

Configuration operators configure all the devices on a headstage, miniscope, or
breakout board in a single step. They belong in the configuration chain between
[CreateContext](xref:OpenEphys.Onix1.CreateContext) and
[StartAcquisition](xref:OpenEphys.Onix1.StartAcquisition).

Each piece of ONIX hardware contains one or more devices. Devices are physical
elements that interface with the environment (e.g., a BNO055 orientation sensor,
a Neuropixels probe, or an RHS2116 stimulus trigger) or internal data sources
(e.g., the port status controller). [Individual device configuration
operators](xref:device-configure) are also available for cases where per-device
control is needed, but most workflows use the combined operators documented
here.

---
uid: device-configure
title: Device Configuration Operators
---

> [!TIP]
>  Device configuration operators are not recommended for using off-the-shelf Open Ephys hardware.
>  Use [device group configuration operators](xref:configure) instead. They confer the following benefits:
> - The `address` and `name` properties of device group configuration operators undergo automatic configuration which reduces the risk of erroneous configuration.
> - The workflow is less cluttered with configuration operators as one device group configuration operator corresponds to multiple device operators. This improves workflow legibility and expedites the workflow scripting process.

Device configuration operators belong in a top-level chain of operators between [`CreateContext`](xref:OpenEphys.Onix1.CreateContext) and [`StartAcquisition`](xref:OpenEphys.Onix1.StartAcquisition) to configure devices contained by ONIX hardware hubs.
---
uid: property-categories
title: Property Categories
---

There are specific categories of properties that define when an operator's properties can be modified. 

`Configuration` properties only have effect when a workflow is started and are used to initialize the hardware state. If they are changed while a workflow is running they will have no effect.

`Acquisition` properties can be manipulated when the workflow is running and will have an immediate effect on hardware. For instance stimulus waveform parameters can be modified in real-time and sent to the device multiple times while the workflow is running to shape stimulation patterns.

`Devices` properties refer to the individual devices available within a particular aggregate operator. Aggregate operators include <xref:OpenEphys.Onix1.ConfigureHeadstage64>, <xref:OpenEphys.Onix1.ConfigureBreakoutBoard>, and more. Explore other available options under the [aggregate configuration operators](xref:configure) page.
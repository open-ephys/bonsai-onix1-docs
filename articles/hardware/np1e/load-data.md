---
uid: np1e_load-data
title: Load Data
---

The following python script can be used to load and plot the data produced by the NeuropixelsV1e
Headstage [example workflow](xref:np1e).

If the [OrderByDepth](#np1e_np1) property is set to `False`, then channels will be ordered by channel
number (i.e., from 0 to 383). If it is set to `True`, then channels will be ordered by the
electrode depth.

[!code-python[](../../../workflows/hardware/np1e/load-np1e.py)]

> [!NOTE]
> - To plot probeinterface data, [save the probe configuration file](xref:np1e_gui#save-probeinterface-file) 
>   into the same directory of your data.
> - This script will attempt to load entire files into arrays. For long recordings, data will need to
>   be split into more manageable chunks by:
>   - Modifying this script to partially load files
>   - Modifying the workflow to cyclically create new files after a certain duration

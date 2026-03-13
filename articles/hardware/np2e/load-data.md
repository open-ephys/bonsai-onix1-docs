---
uid: np2e_load-data
title: Load Data
---

The following python script can be used to load and plot the data produced by the NeuropixelsV2e
Headstage [example workflow](xref:np2e).

If the [OrderByDepth](#np2e_np2) property is set to `False`, then channels will be ordered by channel
number (i.e., from 0 to 383). If it is set to `True`, then channels will be ordered by the
electrode depth.

[!code-python[](../../../workflows/hardware/np2e/load-np2e.py)]

> [!NOTE]
> - To plot probeinterface data, [save the probe configuration file](xref:np2e_gui#save-probeinterface-file) 
>   into the same directory of your data.
> - By default, this script only populates plots for the Neuropixels 2.0 probe A and leaves plots
>   for Neuropixels 2.0 probe B empty. If you are recording from both probes and want to plot probe
>   B ephys and probe data, uncomment the relevant lines in the script.
> - This script will attempt to load entire files into arrays. For long recordings, data will need to
>   be split into more manageable chunks by:
>   - Modifying this script to partially load files
>   - Modifying the workflow to cyclically create new files after a certain duration

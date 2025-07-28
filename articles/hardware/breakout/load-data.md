---
uid: breakout_load-data
title: Load Data
---

The following python script can be used to load and plot the data produced by the Breakout Board [example workflow](xref:breakout_workflow).

[!code-python[](../../../workflows/hardware/breakout/load-breakoutboard.py)]

> [!NOTE]
> This script will attempt to load entire files into arrays. For long recordings, data will need to
> be split into more manageable chunks by:
> - Modifying this script to partially load files
> - Modifying the workflow to cyclically create new files after a certain duration

---
uid: breakout_load-data
title: Load Data
---

The following python script can be used to load and plot the data produced by the Breakout Board [example workflow](xref:breakout_workflow).

> [!NOTE]
> Previous versions of the example workflow used CsvWriter instead of MatrixWriter to write digital
> input data. You can download the script for loading digital data saved using CsvWriter 
> <a href="/workflows/hardware/breakout/load-breakoutboard_csvwriter-digital-inputs.py"
> download>here</a>. With that said, using the updated example workflow is recommended because the
> resulting data occupies less storage.


[!code-python[](../../../workflows/hardware/breakout/load-breakoutboard.py)]

> [!NOTE]
> This script will attempt to load entire files into arrays. For long recordings, data will need to
> be split into more manageable chunks by:
> - Modifying this script to partially load files
> - Modifying the workflow to cyclically create new files after a certain duration

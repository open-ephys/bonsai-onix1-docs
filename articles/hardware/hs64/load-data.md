---
uid: hs64_load-data
title: Load Data
---

The following python script can be used to load and plot the data produced by the Headstage 64
[example workflow](xref:hs64_workflow). It can also be explored in a Google Colab where example data
is available and the Python environment builds reliably.

> [!TIP]
> You will have to change the directory of the data files when using this script for your data.

[!code-python[](../../../workflows/hardware/hs64/load-hs64.py)]

> [!NOTE]
> This script will attempt to load entire files into arrays. For long recordings, data will need to
> be split into more manageable chunks by:
> - Modifying this script to partially load files
> - Modifying the workflow to cyclically create new files after a certain duration

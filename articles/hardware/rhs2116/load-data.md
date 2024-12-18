---
uid: rhs2116_load-data
title: Load Data
---

The following python script can be used to load and plot the data produced by the Headstage Rhs2116 [example workflow](xref:rhs2116).

[!code-python[](../../../workflows/hardware/rhs2116/load-rhs2116.py)]

> [!NOTE]
> This script will attempt to load entire files into arrays. For long recordings, data will need to
> be split into more manageable chunks by:
> - Modifying this script to partially load files
> - Modifying the workflow to cyclically create new files after a certain duration

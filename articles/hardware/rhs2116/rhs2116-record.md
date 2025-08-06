---
uid: rhs2116_record
title: Rhs2116 Recording
---

The following excerpt from the HeadstageRhs2116 [example workflow](xref:rhs2116)
demonstrates the Rhs2116 recording functionality by streaming and saving data
from the Rhs2116 device.

::: workflow
![/workflows/hardware/rhs2116/rhs2116-record.bonsai workflow](../../../workflows/hardware/rhs2116/rhs2116-record.bonsai)
:::

The <xref:OpenEphys.Onix1.Rhs2116PairData> operator generates a sequence of
[Rhs2116PairDataFrames](xref:OpenEphys.Onix1.Rhs2116DataFrame) using the following
settings:
- The BufferSize property is set to 30. Each `Rhs2116PairDataFrame` will contain a
  [1 x 30 sample] Clock vector, a [32 channel x 30 sample] AmplifierData matrix,
  a [32 channel x 30 sample] DcData matrix, and [1 channel x 30 sample] recovery
  mask vector. This corresponds to 1 ms of data per data frame.
- The DeviceName property is set to "HeadstageRhs2116/Rhs2116". This links
  `Rhs2116PairData` to the Rhs2116s on the Headstage Rhs2116.

The relevant properties are extracted from the <xref:OpenEphys.Onix1.Rhs2116PairDataFrame> by
right-clicking the `Rhs2116PairData` operator, and choosing the following Output members: Clock,
AmplifierData, and DcData. The [MatrixWriters](xref:Bonsai.Dsp.MatrixWriter) save the selected
members to files with the following formats: `rhs2116pair-clock_<filecount>.raw`,
`rhs2116pair-ac_<filecount>.raw`, `rhs2116pair-dc_<filecount>.raw`, and
`rhs2116pair-recovery_<filecount>.raw` respectively.

> [!TIP]
> For more details about configuring the Rhs2116 and its data, read the
> [datasheet](https://intantech.com/files/Intan_RHS2116_datasheet.pdf).
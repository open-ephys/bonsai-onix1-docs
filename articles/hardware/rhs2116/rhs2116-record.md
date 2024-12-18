---
uid: rhs2116_record
title: Rhs2116 Recording
---

The following excerpt from the HeadstageRhs2116 [example workflow](xref:rhs2116) demonstrates the Rhs2116
recording functionality by streaming and saving data from the Rhs2116 device.

::: workflow
![/workflows/hardware/rhs2116/rhs2116-record.bonsai workflow](../../../workflows/hardware/rhs2116/rhs2116-record.bonsai)
:::

The <xref:OpenEphys.Onix1.Rhs2116Data> operator generates a sequence of <xref:OpenEphys.Onix1.Rhs2116DataFrame>s using
the following settings:
- `BufferSize` is set to 30. Each `Rhs2116DataFrame` will contain a [1 x 30 sample] `Clock` vector, a [32 channel x 30
  sample] `AmplifierData` matrix, and a [3 channel x 30 sample] `AuxData` matrix. This corresponds to 1.2 ms of data per
  data frame.
- `DeviceName` is set to "HeadstageRhs2116/Rhs2116". This links the `Rhs2116Data`
  operator to the corresponding configuration operator.

The relevant properties are extracted from the `Rhs2116DataFrame` by right-clicking the `Rhs2116Data` operator, and
choosing the following Output members: `Clock`, `AmplifierData`, and `DcData`. The
<xref:Bonsai.Dsp.MatrixWriter> operators saves the selected members to
files with the following format: `rhs2116pair-clock_<filecount>.raw`, `rhs2116pair-dc_<filecount>.raw`, and
`rhs2116pair-ac_<filecount>.raw`, respectively.

> [!TIP] 
> For more details about configuring the Rhs2116 and its data, read the
> [datasheet](https://intantech.com/files/Intan_RHS2116_datasheet.pdf). 
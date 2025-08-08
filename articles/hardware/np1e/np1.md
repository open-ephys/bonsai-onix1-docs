---
uid: np1e_np1
title: NeuropixelsV1e Headstage Neuropixels 1.0 Probe
hardware: NeuropixelsV1e Headstage
---

The following excerpt from the NeuropixelsV1e Headstage [example workflow](xref:np1e) demonstrates Neuropixels 1.0 probe
functionality by streaming and saving probe data.

::: workflow
![/workflows/hardware/np1e/np1.bonsai workflow](../../../workflows/hardware/np1e/np1.bonsai)
:::

The <xref:OpenEphys.Onix1.NeuropixelsV1eData> operator generates a sequence of
[NeuropixelsV1DataFrames](xref:OpenEphys.Onix1.NeuropixelsV1DataFrame) using the following
properties settings:
- `BufferSize` is set to 36. Therefore, each frame will contain a [1 x 36 sample] `Clock` vector, a [384
  channel x 36 sample] `SpikeData` matrix, and a [384 channel x 3 sample] `LfpData` matrix. The Neuropixels 1.0 probe
  samples AP data at 30 kHz per channel (LFP data is sampled at a rate of 1/12 of the rate AP data) so this corresponds
  to 1.2 ms of data.
- `DeviceName` is set to "HeadstageNeuropixelsV1e/NeuropixelsV1e". This links the `NeuropixelsV1eData` operator to the
  corresponding configuration operator.

Given the settings above, each frame will contain a [1 x 36 sample] `Clock` vector, a [384 channel x 36 sample]
`SpikeData` matrix, and a [384 channel x 3 sample] `LfpData` matrix. This corresponds to 1.2 ms of data per data
frame. `LfpData` has less samples than `Clock` and `SpikeData` because `LfpData` is sampled at a lower rate; AP data
is sampled at 30 kHz while LFP data is sampled at 2.5 kHz.

The relevant members are selected from the `NeuropixelsV1DataFrame` by right-clicking the `NeuropixelsV1eData` operator
and choosing the following Output members: `Clock`, `SpikeData`, and `LfpData`. The
[MatrixWriter](xref:Bonsai.Dsp.MatrixWriter) operators save the selected members to files with the following format:
`np1-clock_<filecount>.raw`, `np1-spike_<filecount>.raw`, and `np1-lfp_<filecount>.raw`, respectively.

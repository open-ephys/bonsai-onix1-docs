---
uid: np1e_np1
title: NeuropixelsV1e Headstage Neuropixels 1.0 Probe
hardware: NeuropixelsV1e Headstage
---

The following excerpt from the NeuropixelsV1e Headstage [example workflow](xref:np1e) demonstrates Neuropixels 1.0 probe functionality by streaming and saving probe data.

::: workflow
![/workflows/hardware/np1e/np1.bonsai workflow](../../../workflows/hardware/np1e/np1.bonsai)
:::

The <xref:OpenEphys.Onix1.NeuropixelsV1eData> operator generates a sequence of <xref:OpenEphys.Onix1.NeuropixelsV1DataFrame>s using the following settings:
- `BufferSize` is set to 36.
- The `NeuropixelsV1eData`'s `DeviceName` property is set to "NeuropixelsV1eHeadstage/NeuropixelsV1e". This links the <xref:OpenEphys.Onix1.NeuropixelsV1eData> operator to the corresponding configuration operator.

Given the settings above, each frame will contain a [1 x 36 sample] `Clock` vector, a [384 channel x
  36 sample] `SpikeData` matrix, and a [384 channel x 3 sample] `LfpData` matrix. This corresponds to 1.2 ms of data per data frame.
  `LfpData` has less samples than `Clock` and `SpikeData` because `LfpData` is sampled at a lower rate; AP data is sampled at 30 kHz while LFP data is sampled at 2.5 kHz.

The relevant properties are extracted from the <xref:OpenEphys.Onix1.NeuropixelsV1DataFrame> by right-clicking the <xref:OpenEphys.Onix1.NeuropixelsV1eData> operator, and choosing the following **Output** members: `Clock`, `SpikeData`, and `LfpData`. The [`MatrixWriter`](https://bonsai-rx.org/docs/api/Bonsai.Dsp.MatrixWriter.html) operators saves the selected members to files with the following format: `np1-clock_<filecount>.raw`, `np1-spike_<filecount>.raw`, and `np1-lfp_<filecount>.raw`, respectively.

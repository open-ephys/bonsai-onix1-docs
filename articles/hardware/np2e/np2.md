---
uid: np2e_np2
title: NeuropixelsV2e Headstage Neuropixels 2.0 Probe(s)
hardware: NeuropixelsV2e Headstage
---

> [!NOTE] 
> The NeuropixelsV2eBeta Headstage functions nearly identically to the NeuropixelsV2e Headstage. Simply replace
> `NeuropixelsV2eData` with `NeuropixelsV2eBetaData` and set its `DeviceName` property to
> "HeadstageNeuropixelsV2eBeta/NeuropixelsV2eBeta". 

The following excerpt from the NeuropixelsV2e Headstage [example workflow](xref:np2e) demonstrates Neuropixels 2.0 probe
functionality by streaming data and saves Neuropixels 2.0 probe data. The second chain is disabled by default, assuming
that only one probe is connected to the headstage. If two probes are connected, the second `NeuropixelsV2eData` chain
can be enabled to stream data from both probes simultaneously. To enable, select all nodes in the disabled chain and
press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>D</kbd>, or click `Enable` right-clicking the selected nodes.

::: workflow
![/workflows/hardware/np2e/np2.bonsai workflow](../../../workflows/hardware/np2e/np2.bonsai)
:::

The <xref:OpenEphys.Onix1.NeuropixelsV2eData> operator generates a sequence of
<xref:OpenEphys.Onix1.NeuropixelsV2eDataFrame>s using the following properties settings:
- `BufferSize` is set to 30. Therefore, each frame will contain a [1 x 30 sample] `Clock` vector and a [384 channel x 30
  sample] `AmplifierData` matrix. The Neuropixels 2.0 probe samples at 30 kHz per channel so this corresponds to 1 ms of
  data.
- `DeviceName` is set to "HeadstageNeuropixelsV2e/NeuropixelsV2e". This links the `NeuropixelsV2eData` operator to the
  corresponding configuration operator. 
- `ProbeIndex` is set to "ProbeA". This links the data generated by this probe to the probe in port A of the headstage. 

The relevant members are selected from the `NeuropixelsV2eDataFrame` by right-clicking the `NeuropixelsV2eData`
operator and choosing the following Output members: `Clock`, and `AmplifierData`. The
[MatrixWriter](xref:Bonsai.Dsp.MatrixWriter) operators save the selected members to
files with the following format: `np2-a-clock_<filecount>.raw` and `np2-a-amp<filecount>.raw`, respectively.

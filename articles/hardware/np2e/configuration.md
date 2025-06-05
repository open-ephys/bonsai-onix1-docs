---
uid: np2e_configuration
title: NeuropixelsV2e Headstage Configuration
hardware: NeuropixelsV2e Headstage
configuration: true
operator: ConfigureHeadstageNeuropixelsV2e
dataRate: 18.1
timeUntilFullBuffer: 440 μs
blockReadSize: 8192
workflowLocation: overview
---

> [!NOTE] 
> The NeuropixelsV2eBeta Headstage functions nearly identically to the NeuropixelsV2e
> Headstage. Simply replace `ConfigureHeadstageNeuropixelsV2e` with
> `ConfigureHeadstageNeuropixelsV2eBeta`.

## Configuring the NeuropixelsV2e headstage
The `HeadstageNeuropixelsV2e` operator is set to configure the NeuropixelsV2e Headstage; this can
enable streaming of electrophysiology data from a Neuropixels 2.0 probe and orientation data from a
Bno055 IMU. This is accomplished in the NeuropixelsV2e Headstage example workflow by leaving all of
the `HeadstageNeuropixelsV2e` properties set to their default values.

Default values for the headstage are:
- Enabling the first 384 electrodes of the first shank for streaming (shank 0, electrodes 0 through 383)
    - This is also known as the **Shank 0 Bank A** `Channel Preset`
- Setting `Reference` to *External*
- Setting `Invert Polarity` to `True`

> [!IMPORTANT] 
> The workflow will not run unless gain correction files are provided. Click the
> `HeadstageNeuropixelsV2e` operator, expand `NeuropixelsV2e` in the property pane, then choose the
> appropriate files by selecting either `GainCalibrationFileA` or `GainCalibrationFileB` and
> clicking the <kbd>...</kbd> button. If only one probe is plugged in, only one file is required.

> [!TIP] 
> For additional details on how to manually configure the headstage, such as enabling
> specific electrodes for recording, or modify AP / LFP gain, check out the <xref:np2e_gui> page.

[!INCLUDE [timestamp-info](../../../includes/configuration-timestamp.md)]
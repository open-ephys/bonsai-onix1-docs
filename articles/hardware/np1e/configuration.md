---
uid: np1e_configuration
title: NeuropixelsV1e Headstage Configuration
hardware: NeuropixelsV1e Headstage
configuration: true
operator: ConfigureHeadstageNeuropixelsV1e
dataRate: 20.6
timeUntilFullBuffer: 400 μs
blockReadSize: 8192
workflowLocation: overview
---

## Configuring the NeuropixelsV1e Headstage
The `HeadstageNeuropixelsV1e` operator is used to configure the Neuropixels V1e Headstage; this can enable streaming of electrophysiology data from a Neuropixels 1.0 probe and orientation data from a Bno055 IMU. This is accomplished in the example workflow by leaving all of the `HeadstageNeuropixelsV1e` properties set to their default values.

Default values for the headstage are:
- Enabling the first 384 electrodes for streaming (electrodes 0 through 383)
    - This is also known as the **Bank A** `Channel Preset`
- Setting `AP Gain` to 1000x
- Setting `LFP gain` to 50x
- Setting `Spike Filter` to `True`
- Setting `Reference` to *External*
- Setting `Invert Polarity` to `True`

> [!IMPORTANT]
> The workflow will not run unless gain calibration and ADC calibration files are provided. Click the `HeadstageNeuropixelsV1e` operator, expand `NeuropixelsV1e` in the properties pane, then choose the appropriate files by selecting either `GainCalibrationFile` or `AdcCalibrationFile` and clicking the <kbd>...</kbd> button.

> [!TIP]
> For additional details on how to manually configure the headstage, such as enabling specific electrodes for recording, or modify AP / LFP gain, check out the <xref:np1e_gui> page.

[!INCLUDE [timestamp-info](../../../includes/configuration-timestamp.md)]
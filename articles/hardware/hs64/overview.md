---
uid: hs64_hs64
title: Headstage 64
---

These are the devices available on the Headstage64:

- [Rhd2164](xref:hs64_rhd2164):
    - 64 electrophysiology channels for passive probes (e.g. tetrode, silicon probe, etc.) sampled at 30 kHz with 16 bit depth
    - Adjustable analog band-pass filter:
      - Lower cutoff configurable from 0.1 Hz to 500 Hz
      - Upper cutoff configurable from 100 Hz to 20 kHz
    - Optional adjustable digital high-pass filter with cutoff configurable from 0.146 Hz to 3309 Hz
    - Three auxiliary ADC channels sampled at 30 kHz with 16 bit depth
- [Bno055](xref:hs64_bno055): 9-axis IMU for real-time, 3D orientation tracking sampled up to ~100 Hz for easy automated commutation with Open Ephys commutators
- [Ts4231](xref:hs64_ts4231): For compatibility with HTC Vive Lighthouses for real-time, 3D position tracking sampled at 30 Hz in ideal conditions
- [Electrical Stimulation](xref:hs64_estim): Single current source with ±15V compliance voltage and automatic electrode discharge
    - The stimulation waveform is highly configurable via the <xref:OpenEphys.Onix1.Headstage64ElectricalStimulatorTrigger>'s properties.
- [Optical Stimulation](xref:hs64_ostim): Two current sources with 800mA upper limit
    - The stimulation waveform is highly configurable via the <xref:OpenEphys.Onix1.Headstage64OpticalStimulatorTrigger>'s properties.

> [!TIP]
> For a detailed explanation of the Rhd2164 amplifier's properties, read the [datasheet](https://intantech.com/files/Intan_RHD2164_datasheet.pdf). 

> [!TIP]
> Visit the [Headstage64 Hardware Guide](https://open-ephys.github.io/onix-docs/Hardware%20Guide/Headstages/headstage-64/index.html) to learn more about the hardware such as weight, dimensions, and proper power voltages.

The following pages in the Headstage64 Guide provide an example workflow and a
breakdown of its components.
---
uid: rhs2116
uid: rhs2116
title: Headstage Rhs2116
---

These are the devices available on the Headstage Rhs2116:

- [Rhs2116 Pair](xref:rhs2116):
  - 32 electrophysiology channels that are independently configurable to record electrophysiological signals from or
  deliver electrical stimuli to passive probes.
    - 30193.2367 Hz sample rate with 16 bit depth
    - Adjustable analog band-pass filter:
      - Lower cutoff configurable from 0.1 Hz to 1 kHz
      - Upper cutoff configurable from 100 Hz to 20 kHz
      - Lower cutoff during recovery immediately after stimulus configurable from 0.1 Hz to 1 kHz
    - Optional adjustable digital high-pass filter with cutoff configurable from 0.146 Hz to 3.309 kHz
- [Electrical Stimulation](xref:rhs2116_stimulate): Single current source with ±15V compliance voltage and automatic electrode discharge
    - The stimulation waveform is highly configurable via the <xref:OpenEphys.Onix1.Headstage64ElectricalStimulatorTrigger>'s properties.

> [!TIP]
> Visit the 
> [Headstage Rhs2116 Hardware Guide](https://open-ephys.github.io/onix-docs/Hardware%20Guide/Headstages/headstage-rhs2116.html) 
> to learn more about the hardware such as weight, dimensions, and proper power voltages.

::: workflow
![/workflows/hardware/rhs2116/rhs2116.bonsai workflow](../../../workflows/hardware/rhs2116/rhs2116.bonsai)
:::

The following pages in the Headstage Rhs2116 Guide provide a breakdown of the above example workflow.
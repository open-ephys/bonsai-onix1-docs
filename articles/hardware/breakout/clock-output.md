---
uid: breakout_clock-output
title: Breakout Board Clock Output
hardware: true
device: clock output
---

The output clock is useful for driving external hardware in sync with data
acquisition (e.g. a camera that accepts a "TTL" input to trigger
exposure). The output clock has the following physical properties:

- Real-time clock gate
- Frequency range: 0.1 Hz to 10 MHz
- Start delay: 0 to 3600 seconds
- Duty Cycle: 10 - 90%
- Output impedance: 50 Ohms
- Output current drive: 64mA

> [!TIP]
> For performance at high frequencies (above ~100 kHz), a 50-Ohm coaxial cable
> should be used it the signal should be terminated into 50-Ohms to prevent
> reflections. The high output current drive makes this clock capable of driving
> long cables.

These can all be configured using the <xref:OpenEphys.Onix1.ConfigureBreakoutBoard> operator.
In the example workflow, the output clock is configured to produce a 1 MHz, 50%
duty cycle clock whose start time, phase, and frequency is hardware synchronized
with the ONIX [Acquisition
Clock](xref:OpenEphys.Onix1.ContextTask.AcquisitionClockHz).

Because the clock is generated using a simple frequency divider, not all
configuration settings can be exactly realized in hardware. For this reason, the
following excerpt from the breakout board [example
workflow](xref:breakout_workflow) demonstrates how to save the
[hardware-realized clock parameters](xref:OpenEphys.Onix1.OutputClockParameters)
to a csv file.

::: workflow
![/workflows/hardware/breakout/clock-output.bonsai workflow](../../../workflows/hardware/breakout/clock-output.bonsai)
:::


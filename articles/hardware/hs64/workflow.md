---
uid: hs64_workflow
title: Headstage 64 Example Workflow
---

The example workflow below can by copy/pasted into the Bonsai editor using the clipboard icon in the top right. This workflow:
- Captures electrophysiology data from passive probes via the RHD2164 amplifier and saves it to disk.
- Captures orientation data from the Bno055 IMU and saves it to disk.
- Monitors the Headstage 64 port status.
- Automatically commutates the tether if there is a proper commutator connection. 
- Applies electrical stimulation triggered by pressing the breakout board's △ key.
- Applies optical stimulation triggered by pressing the breakout board's ◯ key.
- Applies both stimulation types with a lower latency trigger mechanism by pressing the breakout board's X key.
- Monitors memory usage data.

::: workflow
![/workflows/hardware/hs64/hs64.bonsai workflow](../../../workflows/hardware/hs64/hs64.bonsai)
:::

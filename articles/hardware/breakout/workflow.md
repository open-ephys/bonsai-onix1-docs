---
uid: breakout_workflow
title: Breakout Board Example Workflow
---

In the following example workflow, we will explore all of the breakout board's
functionality. The workflow below can by copy/pasted into the Bonsai editor
using the clipboard icon in the top right. This workflow:

- Captures data from the breakout board's analog and digital inputs and streams them to disk.
- Generates signals to drive the breakout board's analog and digital outputs.
- Receives synchronization messages from the integrated [Harp](https://harp-tech.org/) input.
- Controls the clock output for driving synchronizing external hardware with data acquisition.
- Monitors and saves hardware memory buffer use information.
- Monitors the breakout board's heartbeat signal.

::: workflow
![/workflows/hardware/breakout/breakout.bonsai workflow](../../../workflows/hardware/breakout/breakout.bonsai)
:::

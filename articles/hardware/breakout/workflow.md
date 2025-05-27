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

> [!IMPORTANT]
> This workflow takes advantage of the MatrixWriter operator's "UnmanagedType" overload available in
> Bonsai 2.9+. [Update your Bonsai to 2.9+](https://bonsai-rx.org/docs/articles/installation.html)
> and [update your to the latest OpenEphys.Onix1](../../getting-started/install-configure-bonsai.md#update-packages)
> to run this workflow.

::: workflow
![/workflows/hardware/breakout/breakout.bonsai workflow](../../../workflows/hardware/breakout/breakout.bonsai)
:::

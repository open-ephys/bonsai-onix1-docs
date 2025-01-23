---
uid: script-workflow
title: Bonsai Workflow Editor
---

Scripting in Bonsai involves placing nodes onto the workflow editor. This page describes how to do
that using <xref:OpenEphys.Onix1.CreateContext> as an example.

1. From the Bonsai editor, navigate to the toolbox on the left side of the screen and expand the **Source** section. Next, expand the **OpenEphys.Onix1** section, and find the `CreateContext` line. The operator can then be added by either double-clicking it, or dragging and dropping the operator into the workflow.

    ![Search for CreateContext operator manually](../../images/bonsai-editor-place-create-context-manually.png){width=700px}

2. Click on the textbox at the top of the toolbox on the left, or from Ctrl + E to focus on the textbox, and type `CreateContext` to search for the operator. Same as (1), the operator can be placed by double-clicking or dragging and dropping; additionally, if the `CreateContext` string is highlighted Enter can be pressed to place the operator immediately.

    ![Search for CreateContext operator from textbox](../../images/bonsai-editor-place-create-context-search.png){width=700px}

3. Hover over the image of the `CreateContext` workflow below, and click on the clipboard icon in the top-right corner of the workflow image to copy the workflow to the clipboard. Navigate back to Bonsai, and paste the copied workflow into the active editor. Pasting can be done via Ctrl + V, or right-clicking in the editor and choosing **Paste**.

## CreateContext Workflow

This is a nominally functional workflow that provides access to the ONI context, from which all operators can then be linked to and configured, while also demonstrating how a Breakout Board can be configured before finishing the configuration chain by placing a [StartAcquisition](xref:OpenEphys.Onix1.StartAcquisition) operator:

:::workflow 
![CreateContext](../../workflows/operators/ConfigureBreakoutBoard.bonsai)
:::

---
uid: bonsai-workflows
title: Bonsai Workflows
---

A Bonsai **workflow** is a graph of connected **operators**, each of which
produces, transforms, or acts on a stream of data. Data flows left to right:
each operator receives the output of the operator to its left as input. The
role of an operator depends on its type:

- A `source` operator generates a sequence of data (e.g. from a hardware device).
- A `transform` operator converts each element it receives.
- A `sink` operator uses incoming data to produce an external effect, such as
  saving to disk or toggling a digital output. Its output is identical to its
  input.
- A `combinator` operator merges, splits, gates, or otherwise controls the flow
  of one or more sequences.

These classifications are represented in the workflow editor using different
colored nodes. The [official Bonsai
docs](https://bonsai-rx.org/docs/articles/operators.html) provides a detailed
description of operators and the various types with pictures.

Below is an example workflow which configures ONIX hardware.

::: workflow
![/workflows/getting-started/start-acquisition.bonsai workflow](../../workflows/getting-started/start-acquisition.bonsai)
:::

> [!TIP]
> This workflow, and others like it in these docs, can be copied and pasted into
> the Bonsai editor using the clipboard icon that appears when you hover your
> mouse over the image.

We'll take a closer look at how this workflow is created and what it's used for
in the following pages.
---
uid: operator-types
title: Operator Types
---

In Bonsai, a "workflow" is composed of ["operators"](https://bonsai-rx.org/docs/articles/operators.html) that are connected together to form a data processing graph. Each operator is classified into as a `Source`, `Transform`, `Condition`, `Sink`, or `Combinator` based upon how it behaves. ONIX operators fall in the following categories:

| Operator Type | Description | Example ONIX operators |
| --------- | ----------- | ------------------ |
| Source    | Generate acquisition state or hardware data | [CreateContext](xref:OpenEphys.Onix1.CreateContext), [Bno055Data](xref:OpenEphys.Onix1.Bno055Data), [NeuropixelsV1eData](xref:OpenEphys.Onix1.NeuropixelsV1eData) |
| Sink      | Configure and send data to hardware | [ConfigureHeadstage64](xref:OpenEphys.Onix1.ConfigureHeadstage64), [ConfigureNeuropixelsV1eHeadstage](xref:OpenEphys.Onix1.ConfigureNeuropixelsV1eHeadstage) |
| Combinator | Manage control flow | [StartAcquisition](xref:OpenEphys.Onix1.StartAcquisition) |

---
uid: reference
title: Software Reference
---

The following table provides information about which operators correspond to which hardware and the "Offset" and "Scale"
values to convert the ADC value to μV. "Offset" refers to the value required to subtract from unsigned data to center
its dynamic range around zero. It's typically $-2^{(bitDepth - 1)}$ for unsigned data. "Scale" refers to the scalar
required to multiply to your data to convert it from units of DAC/ADC step size to μV.

<!--
- Column select (i.e. Alt+Shift on VS Code) can be extremely helpful for editing this table
- Remove any white space at end of table after pipe symbol (|) or else DocLinkChecker will complain
-->

| Analog Device                                                                                                               |Bit Depth | Offset | Scale/Step Size (μV/bit)                                                                                                | Relevant Data Operator                        | Data Frame                                         | Relevant Hardware                                                                                                                    | Relevant Configuration Operator(s)                                                 |
|-----------------------------------------------------------------------------------------------------------------------------|----------|--------|-------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------|----------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| [Intan Rhd2164 (amplifier & auxiliary)](https://intantech.com/files/Intan_RHD2164_datasheet.pdf)                            | 16       | -32768 | 0.195                                                                                                                   | <xref:OpenEphys.Onix1.Rhd2164Data>            | <xref:OpenEphys.Onix1.Rhd2164DataFrame>            | [Headstage 64](https://open-ephys.github.io/onix-docs/Hardware%20Guide/Headstages/headstage-64/index.html)                           | <xref:OpenEphys.Onix1.ConfigureHeadstage64>                                        |
| [Intan Rhs2116 (AC)](https://intantech.com/files/Intan_RHS2116_datasheet.pdf)                                               | 16       | -32768 | 0.195                                                                                                                   | <xref:OpenEphys.Onix1.Rhs2116Data>            | <xref:OpenEphys.Onix1.Rhs2116DataFrame>            | [Headstage Rhs2116](https://open-ephys.github.io/onix-docs/Hardware%20Guide/Headstages/headstage-rhs2116.html)                       | <xref:OpenEphys.Onix1.ConfigureHeadstageRhs2116>                                   |
| [Intan Rhs2116 (DC)](https://intantech.com/files/Intan_RHS2116_datasheet.pdf)                                               | 10       | -512   | -19230                                                                                                                  | <xref:OpenEphys.Onix1.Rhs2116Data>            | <xref:OpenEphys.Onix1.Rhs2116DataFrame>            | [Headstage Rhs2116](https://open-ephys.github.io/onix-docs/Hardware%20Guide/Headstages/headstage-rhs2116.html)                       | <xref:OpenEphys.Onix1.ConfigureHeadstageRhs2116>                                   |
| [Imec Neuropixels 1.0 probe (AP & LFP)](https://www.neuropixels.org/_files/ugd/328966_c5e4d31e8a974962b5eb8ec975408c9f.pdf) | 10       | -512   | 1.2e6/1024/gain[^1]                                                                                                     | <xref:OpenEphys.Onix1.NeuropixelsV1eData>     | <xref:OpenEphys.Onix1.NeuropixelsV1DataFrame>      | [Headstage Neuropixels V1e](https://open-ephys.github.io/onix-docs/Hardware%20Guide/Headstages/headstage-neuropix-1e.html)           | <xref:OpenEphys.Onix1.ConfigureNeuropixelsV1eHeadstage>                            |
| [Imec Neuropixels 2.0 probe](https://www.neuropixels.org/_files/ugd/328966_2b39661f072d405b8d284c3c73588bc6.pdf)            | 12       | -2048  | 3.0517578125                                                                                                            | <xref:OpenEphys.Onix1.NeuropixelsV2eData>     | <xref:OpenEphys.Onix1.NeuropixelsV2eDataFrame>     | [Headstage Neuropixels V2e](https://open-ephys.github.io/onix-docs/Hardware%20Guide/Headstages/headstage-neuropix-2e.html)           | <xref:OpenEphys.Onix1.ConfigureNeuropixelsV2eHeadstage>                            |
| Imec Neuropixels 2.0 Beta probe                                                                                             | 14       | -8192  | 0.7629                                                                                                                  | <xref:OpenEphys.Onix1.NeuropixelsV2eBetaData> | <xref:OpenEphys.Onix1.NeuropixelsV2eBetaDataFrame> | [Headstage Neuropixels V2e Beta](https://open-ephys.github.io/onix-docs/Hardware%20Guide/Headstages/headstage-neuropix-2e-beta.html) | <xref:OpenEphys.Onix1.ConfigureNeuropixelsV2eBetaHeadstage>                        |
| [Imec Nric 1.0 384](https://www.neuropixels.org/_files/ugd/328966_c59e77054175456cb0c3ef82b32219c1.pdf)                     | 10       | -512   | 1.2e6/1024/gain[^1]                                                                                                     | <xref:OpenEphys.Onix1.Nric1384Data>           | <xref:OpenEphys.Onix1.Nric1384DataFrame>           | Headstage Nric1384                                                                                                                   | <xref:OpenEphys.Onix1.ConfigureHeadstageNric1384>                                  |
| [Breakout Board analog input](https://open-ephys.github.io/onix-docs/Hardware%20Guide/Breakout%20Board/index.html)          | 16       | -32768 | <span style="white-space: nowrap">[analogInputVoltageRange](xref:OpenEphys.Onix1.AnalogIOVoltageRange)/65536</span>[^2] | <xref:OpenEphys.Onix1.AnalogInput>            | <xref:OpenEphys.Onix1.AnalogInputDataFrame>        | [Breakout Board](https://open-ephys.github.io/onix-docs/Hardware%20Guide/Breakout%20Board/index.html)                                | <xref:OpenEphys.Onix1.ConfigureBreakoutBoard>                                      |
| [Breakout Board analog output](https://open-ephys.github.io/onix-docs/Hardware%20Guide/Breakout%20Board/index.html)         | 16       | 0      | 305.17578125 (in "S16" mode)[^3]                                                                                        | <xref:OpenEphys.Onix1.AnalogOutput>           | -                                                  | [Breakout Board](https://open-ephys.github.io/onix-docs/Hardware%20Guide/Breakout%20Board/index.html)                                | <xref:OpenEphys.Onix1.ConfigureBreakoutBoard>, <xref:OpenEphys.Onix1.AnalogOutput> |

[^1]: The Neuropixels 1.0 probes and Imec Nric 1.0 384 amplifier have selectable gain. The appropriate "Scale" value
depends on the chosen gain according to the following formula: 1.2e6/1024/gain. The gain is set by the user in the
[NeuropixelsV1e Headstage Configuration GUI](xref:np1e_gui), for example.

[^2]: The Breakout Board analog input range can be configured to accept ±10 volts, ±5 volts, or ±2.5 volts input range.
The appropriate "Scale" value depends on the chosen analog input voltage range according to the following formula:
[analogInputVoltageRange](xref:OpenEphys.Onix1.AnalogIOVoltageRange)/65536. This voltage range is configured by editing
the <xref:OpenEphys.Onix1.ConfigureBreakoutBoard> operator's `AnalogIO` input range properties and must be configured per
analog input.

[^3]: The Breakout Board analog output can be configured to accept units of volt or DAC step size (305.17578125 μV/bit).
The appropriate "Scale" value is only relevant if you are ouputting in units of volts depends on the chosen analog
output datatype. This datatype is configured by editing <xref:OpenEphys.Onix1.AnalogOutput>'s `DataType` property. This
data is already signed, so no shift is necessary.

> [!TIP]
> - If you are trying to insert the "Offset" value from this table into the "Offset" field in the Open Ephys GUI, insert
>   a positive value. The Open Ephys GUI automatically negates the "Offset" value inserted by the user. 
> - If you are trying to insert the "Offset" and "Scale" values from this table into the "Shift" property and "Scale"
>   property fields of a single <xref:Bonsai.Dsp.ConvertScale> operator in Bonsai, insert the "Offset" value multiplied
>   by the "Scale" value. The `ConvertScale` operator applies the shift transformation after the scale transformation. 
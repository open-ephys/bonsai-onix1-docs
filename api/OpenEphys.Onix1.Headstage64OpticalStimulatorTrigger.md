---
uid: OpenEphys.Onix1.Headstage64OpticalStimulatorTrigger
---

> [!IMPORTANT]
> Headstages manufactured before October 2024 have an optical stimulator that
> behaves differently from those manufactured after that date. On older
> headstages, a `True` value at this operator's input continuously delivers
> stimuli, while a `False` value stops delivery. On newer headstages, a `True`
> value delivers a single stimulus per trigger. Additionally, on older
> headstages, the frequency parameter controls the interval between the end of
> one pulse and the start of the next, meaning the actual repetition rate equals
> the pulse duration plus 1/frequency. If you need to use the optical
> stimulator, you can verify whether you have an older or newer headstage by
> reading back the electrical stimulation waveform from one of the headstage's
> Intan chip's auxiliary inputs. If you have an older headstage and require the
> specific stimulation behavior of a newer headstage, [contact
> us](https://open-ephys.org/contact).

---
uid: OpenEphys.Onix1.Headstage64ElectricalStimulatorTrigger
---

> [!IMPORTANT] 
> Headstages manufactured before October 2024 have an electrical stimulator that
> behaves differently from those manufactured after that date. On older
> headstages, a `True` value at this operator's input continuously delivers
> stimuli, while a `False` value stops delivery. On newer headstages, a `True`
> value delivers a single stimulus per trigger. If you need to use the
> electrical stimulator, you can verify whether you have an older or newer
> headstage by reading back the stimulation waveform from one of the headstage's
> Intan chip's auxiliary inputs. If you have an older headstage and require the
> specific stimulation behavior of a newer headstage, [contact
> us](https://open-ephys.org/contact).

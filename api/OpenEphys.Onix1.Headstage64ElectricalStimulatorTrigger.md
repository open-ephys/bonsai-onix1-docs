---
uid: OpenEphys.Onix1.Headstage64ElectricalStimulatorTrigger
---

> [!IMPORTANT]
> Headstages manufactured before October 2024 have an electrical stimulator that
> behaves differently from those manufactured after that date. On older
> headstages, a `True` value at this operator's input continuously delivers
> stimuli, while a `False` value stops delivery. On newer headstages, a `True`
> value delivers a single stimulus. If your headstage was purchased around the
> transition date and you want to use the electrical stimulator, you can confirm
> whether you have an older or newer headstage by observing the trigger behavior
> on the headstage's Intan chip's auxiliary input, to which the stimulus
> signal is hard-wired. If your headstage exhibits the older trigger behavior
> and you specifically require the newer behavior, [contact
> us](https://open-ephys.org/contact).

---
uid: OpenEphys.Onix1.Headstage64OpticalStimulatorTrigger
---

> [!IMPORTANT]
> Headstages manufactured before October 2024 have an optical stimulator that
> behaves differently from those manufactured after that date. On older
> headstages, a `True` value at this operator's input continuously delivers
> stimuli, while a `False` value stops delivery. On newer headstages, a `True`
> value delivers a single stimulus. Additionally, on older headstages, the
> frequency parameter controls the interval between the end of one pulse and the
> start of the next, meaning the actual repetition rate equals the pulse
> duration plus 1/frequency. If your headstage was purchased around the
> transition date and you want to use the optical stimulator, you can infer your
> headstage version by observing the trigger behavior on the headstage's Intan
> chip's auxiliary input, to which the electrical stimulus signal is hard-wired,
> since the optical stimulator does not have a direct read-back path. The
> trigger behavior is the same for both stimulators. If you have an older
> headstage and require the specific trigger/stimulus behavior of a newer
> headstage, [contact us](https://open-ephys.org/contact).

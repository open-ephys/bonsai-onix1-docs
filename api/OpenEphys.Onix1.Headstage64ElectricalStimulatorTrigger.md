---
uid: OpenEphys.Onix1.Headstage64ElectricalStimulatorTrigger
---

> [!IMPORTANT] 
> Headstages manufactured before approximately September/October 2024 have an
> electrical stimulator that behaves differently from those manufactured after
> that date. On older headstages, a `True` value at this operator's input
> continuously delivers stimuli, while a `False` value stops delivery. On newer
> headstages, a `True` value delivers a single stimulus per trigger. The best
> way to determine which version you have is to probe the headstage with an
> oscilloscope or connect a light source to the optical stimulator and observe
> the behavior. If you have an older headstage and require the specific
> stimulation behavior of a newer headstage, [contact
> us](https://open-ephys.org/contact).

> [!NOTE]
> Early headstages with **v1** electrical and optical stimulators behave
> differently from those with **v2** stimulators. With **v1** stimulators, a
> `True` value at the trigger node's input will continuously deliver stimuli,
> while a `False` value will stop delivery. With **v2** stimulators, a `True`
> value at the trigger node's input delivers a single stimulus. The best way to
> know which stimulator you have is to probe the headstage with an oscilloscope
> and observe the stimulator's behavior. If you need to update your headstage64,
> please contact us through support[at]oeps[dot]tech.
When the workflow is started, the current time (based on 
[Coordinated Universal Time](https://en.wikipedia.org/wiki/Coordinated_Universal_Time))
is saved, along with global hardware parameters governing data acquisition. This is 
accomplished using a [TimeStamp](https://bonsai-rx.org/docs/api/Bonsai.Reactive.Timestamp.html) operator 
to capture the computer's wall clock time. This
`Timestamp` is saved along with `ContextTask`'s properties (e.g.,
`AcquisitionClockHz`, `BlockReadSize`, `BlockWriteSize`) to a csv
file (`start-time_<filecount>.csv`) when the the workflow is started.
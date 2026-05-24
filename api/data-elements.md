---
uid: data-elements
title: Data Elements
---

These pages contain information about data elements that can help interpret and
load data produced by <xref:datasource>.

## DataFrames

<xref:datasource> produce a sequence of either <xref:OpenEphys.Onix1.DataFrame>
or <xref:OpenEphys.Onix1.BufferedDataFrame>, which are `DataFrames` that
contain multiple samples. `DataFrames` comprise timing information along with
corresponding data for a particular device:

- The <xref:OpenEphys.Onix1.DataFrame.Clock> which contains a system-wide
  synchronized clock count value that can be related to the `Clock` property of
  any other data frame collected within a given [ONIX
  Context](xref:OpenEphys.Onix1.CreateContext).
- The <xref:OpenEphys.Onix1.DataFrame.HubClock> property contains the precise
  hardware timestamp created using the local clock on the hardware that contains
  the device (for instance the local oscillator on a given headstage).
- The data payload(s) corresponding to each clock value, e.g. a set
  of analog voltage samples like
  <xref:OpenEphys.Onix1.AnalogInputDataFrame.AnalogData> for the breakout
  board's analog inputs.

## Using DataFrame type information

The data element pages also document the type and size of each property. This
is useful in a few ways:

- **Estimating data rates.** Multiply the per-sample byte count of all
  properties by the device sample rate to get throughput in bytes per second.
  For example, a single <xref:OpenEphys.Onix1.NeuropixelsV2eData> stream
  produces 384 channels of `ushort` (2 bytes each) plus two 8-byte clock
  fields at 30 kHz, giving roughly 23.5 MB/s.

  $$
  \begin{equation}
    \frac{2*384+8+8\,bytes}{sample}*\frac{30,000\,samples}{s}*\frac{1\,MB}{10^6bytes} = 23.52\,MB/s
    \label{eq:1x_npx2_bw}
  \end{equation}
  $$

- **Operator compatibility in Bonsai.** Bonsai operators accept only specific
  types as inputs. If a connection between two nodes produces a type mismatch,
  Bonsai will indicate an error. Knowing a property's type helps diagnose these
  errors and choose the correct downstream operator.

- **Loading raw binary files.** If data was saved with
  <xref:Bonsai.Dsp.MatrixWriter>, the property type determines the correct
  [NumPy dtype](https://numpy.org/doc/stable/reference/arrays.dtypes.html) to
  use when reading the file back. For example, a `Clock` property saved as
  `ulong` requires `dtype=np.uint64` when loading.

  > [!TIP]
  > The <xref:OpenEphys.Onix1.DataFrameWriter.DataFrameWriter> includes all
  > frame type information within the file it writes, so the user does not need
  > to worry about knowing the exact type of each property. See [the
  > tutorial](xref:data-frame-writer) for details on its use.

## Other data elements

Aside from DataFrames, <xref:OpenEphys.Onix1> operators produce:

- <xref:OpenEphys.Onix1.ContextTask>: an object passed through the
  configuration chain for writing to and reading from the ONIX hardware.
- <xref:OpenEphys.Onix1.OutputClockParameters>: the parameters used to
  configure the precise hardware output clock when the workflow starts.

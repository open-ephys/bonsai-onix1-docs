---
uid: visualize-data
title: Data Visualization
---

Bonsai displays data using [type
visualizers](https://bonsai-rx.org/docs/articles/editor.html?#type-visualizers),
windows that plot or inspect the output of an operator in real time.
Double-click any node while the workflow is running to open its visualizer.

## Select data member(s)

Some data types, such as [ONIX data frames](xref:data-elements), are composed of
multiple grouped data elements. It's often useful to be able to select certain
data features from composed types either for downstream processing or
visualization. To select data members in the Bonsai Editor:

1. Right-click the node.
1. Hover the cursor over the "Output" option that appears in the context menu.
1. Click the inner data member you would like to select.

Under the hood, this action produces a
<xref:Bonsai.Expressions.MemberSelectorBuilder> operator that selects a single
member from the output of any operator in the editor.

<video controls>
  <source src="../../images/select-member.mp4" type="video/mp4">
</video>

> [!NOTE]
> Member selection is useful when an operator's output type doesn't have type
> visualizers that allow users to inspect the data in a meaningful capacity.
> This is often the case for [data source operators](xref:datasource) which
> produce [data frames](xref:data-elements) that typically contain multiple
> different data features.

## Select visualizers

Select the visualizer you would like to use for visualizing data:

1. Right-click the node producing the data you would like to visualize.
1. Hover the cursor over the "Select Visualizer" option in the context menu.
1. Click the visualizer you would like to use from the list of visualizers.

<video controls>
    <source src="../../images/set-visualizer.mp4" type="video/mp4">
</video>

At this point, the visualizer should open when the workflow is started.

> [!NOTE]
> If you don't see data in the visualizer, check that:
>
> - The device from which you are trying to read is enabled.
> - The conditions required for the operator to produce data are met. Some
>   operators only produce data in response to external events, rather than at a
>   fixed rate. For example, the <xref:OpenEphys.Onix1.DigitalInput> operator,
>   when no sample rate is configured, only produces data when the digital port
>   status changes state. Similarly, the
>   <xref:OpenEphys.Onix1.TS4231V1PositionData> operator only produces data when
>   the TS4231 receivers are within range of the lighthouse transmitters.

> [!TIP]
> Visualizers can be selected while the workflow is running which is helpful for
> more quickly trying different visualizer options in succession if you are
> unsure about which one you want to use.

## Configure visualizers

Some visualizers, in particular those that involve plots, allow additional
configuration. Right-click the visualizer window to gain access to configuration
options.

For example, the MatVisualizer allows configuration of:

- X and Y scale: click to toggle between "auto" and fixed values.
- Channel view: click the grid square to toggle between superimposed or separate
- History Length: click the arrow and configure the number of samples displayed
  in the plot.
- Display Previous: click the arrow and configure the amount of buffers
  displayed in the plot.
- Channel Offset: click the arrow and configure the Y offset.
- Channels per Page: click the arrow and configure the amount of channels
  displayed per visualizer page. The page number is displayed at the top of the
  visualizer. Move between pages by using the PageUp and PageDn keys on the
  keyboard.

<video controls>
  <source src="../../images/visualize-data.mp4" type="video/mp4">
</video>

> [!TIP]
> For other data visualization options, additional visualizers are available as
> standalone operators and can be found in the `Bonsai.Design.Visualizers`
> package. These visualizer operators must be connected to an operator that
> produces a sequence of compatible data. The visualizer window can be opened by
> double-clicking the visualizer node instead of the preceding data node.

## Next steps

Find and run an example workflow for your particular hardware in the
<xref:data-acq-quick-start>. After that, check out the <xref:tutorials>.
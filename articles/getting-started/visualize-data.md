---
uid: visualize-data
title: Data Visualization
---

Bonsai has "[type visualizers](https://bonsai-rx.org/docs/articles/editor.html?#type-visualizers)"
that display data produced by an operator. They are opened by double-clicking the corresponding node
while the workflow is running. Read below for more details about how to visualize data.

## Select data member(s)

Some operators, such as [ONIX data I/O operators](xref:dataio), require selecting members from their
output to visualize their data:
    1.  Right-click the node that corresponds to the data I/O operator that streams data you'd like to
        visualize.
    1. Hover the cursor over the "Output" option that appears in the context menu.
    1. Click the member you would like to visualize from the list of members.

This populates the workflow with a <xref:Bonsai.Expressions.MemberSelectorBuilder> operator that
selects the single member from the data frame produced by the data I/O operator.

<video controls>
  <source src="../../images/select-member.mp4" type="video/mp4">
</video>

> [!NOTE]
> Member selection is required when an operator's output type doesn't have type visualizers that
> allow users to inspect the data in a meaningful capacity. This is true for [ONIX data I/O
> operators](xref:dataio) which typically produce [data frames](xref:data-elements).

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
> Data will only be visualized if the operator is producing data. If you can't see any data, check
> that:
> - The device from which you are trying to read is enabled.
> - Events are occurring for event-based devices. Event-based devices only produce data upon certain
>   events whereas other operators always producing data. For example, the
>   <xref:OpenEphys.Onix1.DigitalInput> operator only produces data when the digital port status
>   changes state so it is event-based.

> [!TIP]
> Visualizers can be selected while the workflow is running which is helpful for more quickly trying
> different visualizer options in succession if you are unsure about which one you want to use.

## Configure visualizers
Some visualizers, in particular those that involve plots, allow additional configuration.
Right-click the visualizer window to gain access to configuration options.

For example, the MatVisualizer allows configuration of:
-   X and Y scale: click to toggle between "auto" and fixed values.
-   Channel view: click the grid square to toggle between superimposed or separate
-   History Length: click the arrow and configure the number of samples displayed in the plot.
-   Display Previous: click the arrow and configure the amount of buffers displayed in the plot.
-   Channel Offset: click the arrow and configure the Y offset.
-   Channels per Page: click the arrow and configure the amount of channels displayed per visualizer
    page. The page number is displayed at the top of the visualizer. Move between pages by using the
    PageUp and PageDn keys on the keyboard.

<video controls>
  <source src="../../images/visualize-data.mp4" type="video/mp4">
</video>

> [!TIP]
> For other data visualization options, additional visualizers are available as standalone operators
> and can be found in the `Bonsai.Design.Visualizers` package. These visualizer operators must be
> connected to an operator that produces a sequence of compatible data. The visualizer window can be
> opened by double-clicking the visualizer node instead of the preceding data node.

## Next Steps

Find and run an example workflow for your particular hardware in the <xref:data-acq-quick-start>. After that,
check out the <xref:tutorials>.
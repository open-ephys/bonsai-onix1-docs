---
uid: ucla-miniscope-v4_camera
title: UCLA Miniscope v4 Camera Data
---

The following excerpt from the UCLA Miniscope v4 [example workflow](xref:ucla-miniscope-v4) demonstrates the UCLA
Miniscope v4 camera-related functionality by streaming and saving data from the UCLA Miniscope v4 camera and allowing
the user to dynamically modifying camera parameters.

::: workflow
![/workflows/hardware/ucla-miniscope-v4/camera.bonsai workflow](../../../workflows/hardware/ucla-miniscope-v4/camera.bonsai)
:::

The <xref:OpenEphys.Onix1.UclaMiniscopeV4CameraData> operator generates a sequence of
[UclaMiniscopeV4CameraFrames](xref:OpenEphys.Onix1.UclaMiniscopeV4CameraFrame) using the following properties settings:
- `DataType` is set to "U8". This sets the bit depth of each pixel in the image to eight (instead of ten if `DataType`
  is set to "U10")
- `DeviceName` is set to "UclaMiniscopeV4/UclaMiniscopeV4". This links the `UclaMiniscopeV4CameraData` operator to the
  corresponding configuration operator. 

The relevant members are selected from the `UclaMiniscopeV4CameraFrame` by right-clicking the
`UclaMiniscopeV4CameraData` operator and choosing the following Output members: `Camera`, and `Clock`. The
[VideoWriter](xref:Bonsai.Vision.VideoWriter) saves the `Camera` to a files with the following format:
`ucla-miniscope-v4-video_.avi` with "DIB " FourCC. The [MatrixWriter](xref:Bonsai.Dsp.MatrixWriter) saves the `Clock` to a
files with the following format: `ucla-miniscope-v4-clock_.raw`.

> [!NOTE]
> - If you edit the FourCC property yourself and want to use "DIB ", take care to include a space as the fourth character.
> - You can also use the "FMP4" FourCC which compresses the video data into smaller file sizes. However, "FMP4" can only
> be used with 8-bit data.

Try adjusting the `FrameRate`, `SensorGain`, `LEDBrightness`, and `LiquidLensVoltage` properties while the workflow is
running and observing the camera data. Follow our <xref:visualize-data> guide if you are not sure how to observe the
camera data. 
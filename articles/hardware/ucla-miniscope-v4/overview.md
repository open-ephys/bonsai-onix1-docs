---
uid: ucla-miniscope-v4
title: UCLA Miniscope v4
---

These are the devices available on the UCLA Miniscope v4:

- [UCLA Miniscope v4 Camera System](xref:ucla-miniscope-v4_camera) camera sensor:
    - 0.48 Megapixel CMOS 8-bit or 10-bit image sensor (608 x 608 pixels) data
    - Python480 sensor for dynamic adjustment of frame rate in discrete increments: 10, 15, 20, 25 or 30 fps
    - Python480 sensor for dynamic adjustment of exposure in three discrete levels
    - ETL for dynamic and continuous ~500 µm adjustment of imaging depth with off-the-shelf lens configuration
    - LED driver for dynamic and continuous adjustment of excitation light intensity
- [Bno055](xref:ucla-miniscope-v4_bno055): 9-axis IMU for real-time, 3D orientation tracking updated at the same frame
  rate as the camera

> [!TIP]
> Visit the [UCLA Miniscope v4 Hardware Guide](https://open-ephys.github.io/miniscope-docs/ucla-miniscope-v4/index.html) to learn more about the hardware such as weight, dimensions, and proper power voltages.

The example workflow below can by copy/pasted into the Bonsai editor using the clipboard icon in the top right. This workflow:
- Captures image data from the UCLA Miniscope v4 Camera System and saves it to disk.
- Captures orientation data from the Bno055 IMU and saves it to disk.
- Monitors the UCLA Miniscope v4 port status.
- Automatically commutates the tether if there is a proper commutator connection. 

::: workflow
![/workflows/hardware/ucla-miniscope-v4/ucla-miniscope-v4.bonsai workflow](../../../workflows/hardware/ucla-miniscope-v4/ucla-miniscope-v4.bonsai)
:::

The following pages in the UCLA Miniscope v4 Guide provide a breakdown of the above example workflow.
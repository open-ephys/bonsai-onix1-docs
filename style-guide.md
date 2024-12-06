# Style Guide

## General

Follow the style of our other docs sites.

## Articles

- Don't repeat hyperlinks in the same page.
- Try not to overdo formatted text (e.g. a bunch of text wrapped in back ticks can make the page hard to read and look
  at)

## Hardware Guide

- Don't use moon button to trigger because it's used to toggle dark/light mode.
- Use standard names for saving files:
    - specify standard here
- All hardware guides should include loading scripts and ideally example data
- Unify workflows
    - Headstage workflows should contain a ConfigureBreakoutBoard node
    - Headstage workflows should contain a MemoryMonitor node

## Real World Visuals 

- Include visuals of real world actions wherever possible. 
- Click to play videos and gifs.
- No audio in videos.
- When doing screen records, include visual indicator of mouse clicks and keyboard presses.
    - Specify what those indicators look like and how they are done. jonnew likes screen2gif for this.

## File naming standard

- Use same abbreviation across files:
    - Headstage64: hs64
    - NeuropixelsHeadstage1Ve: np1e
    - NeuropixelsHeadstage2Ve: np2e
    - NeuropixelsHeadstage2VeBeta: np2ebeta
    - Neuropixels 1.0 probes: np1
    - Neuropixels 2.0 probes: np2
    - Neuropixels 2.0 Beta probes: np2beta
- 

## Maintaining screenshots

### Creating Edited Screenshots

There are webpages with edited screenshots of Bonsai. The source material (.xcf GIMP files) belongs in the img-src
directory for ease of maintenance. The sections below describe how you can quickly create a new screenshot.

To take the screenshot (in Windows), use the `Windows+Shift+S` hotkey, select the `Window` option, and select the window
you would like to screenshot. The preference is to take a screenshot against a grey background (e.g. create a (R: 127,
G: 127, B: 127) background in GIMP) because some of the background makes it into the screenshot.

### Bonsai Package Manager Screenshot Edits

The layer group consisting of the highlight layer and 1,2,3,4 layers of the screenshots in the bonsai-install\*.xcf or
bonsai-update\*.xcf files can be copy and pasted on top of other screenshots. This enables an expedited editing process
for creating new edited screenshots. When creating the screenshot, do not change the size of the package manager after
opening it.

## Workflows

### Example Workflows in Hardware User Guides

Use "FileCount" for writer operators with a `Suffix` property. This makes loading data easier than using a timestamp
because not all files from a given data acquisition session have the same timestamp.

Consistency here facilitates scripting the data loading Python scripts.

All of these example workflows should contain:
- Top-level configuration motif with the headstage/miniscope *and* the breakout board
    - Timestamp when the headstage/miniscope is configured
    - Write that to CSV
        - `Filename`: "start_time_.csv"
        - `Selector`: "Timestamp,Value"
- Port status graph
    - Timestamp port status changes
    - Write to CSV
        - `Filename`: "port-status_.csv"
        - `Selector`: "Timestamp,Value.Clock,Value.StatusCode"
- Bno055 graph (if relevant)
    - Use the correct Bno node (polled or not)
    - Write to CSV
        - `Filename`: "bno055_.csv"
        - `Selector`: "Clock,EulerAngle,Quaternion,Acceleration,Gravity,Temperature"
    - Select Quaternion data for commutation
    - Connect disabled AutoCommutator node so that people don't need to connect their commutator for the workflow to
      run
- Memory monitor graph. 
    - Select the `PercentUsed` member so the user can monitor memory usage
    - Writing to CSV is not necessary (maybe it'ss helpful for them if need to troubleshoot something, but otherwise
        irrelevant)

> [!NOTE]
> Order of selected members (e.g. using the `Selector` property of the `CsvWriter`) matters for loading data.

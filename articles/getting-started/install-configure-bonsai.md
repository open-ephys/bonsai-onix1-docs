---
uid: install-configure-bonsai
title: Installation
---

## Bonsai Installation

To download Bonsai, select between the portable download and the installer download
[here](https://bonsai-rx.org/docs/articles/installation.html).

*   The **Portable** download (.zip) installs a sand-boxed version of Bonsai. Portable environments
    enable users to switch between different environments to prevent package conflicts or use
    different versions of packages.
    *   To install from the **Portable** download, extract the downloaded file. You can start the
        portable Bonsai by running the `Bonsai.exe` that is inside the extracted folder.
*   The **Installer** download (.exe) installs Bonsai and all its dependencies globally.
    *   To install from the **Installer** download, run the downloaded `Bonsai-X.X.X.exe` file and
        agree to the involved licenses. You can start the globally installed Bonsai by launching it
        from the `Bonsai Setup` window after installing or searching for it in your OS's search
        function, for example. 

> [!TIP]
> When using multiple environments, create and name shortcuts such that different Bonsai
> environments are easier to find and distinguish. 

## Package Installation

Bonsai packages expand the set of operators available to you for building useful workflows. For
example, the `OpenEphys.Onix1` package is required to interface with Onix hardware through Bonsai.

### Open the Bonsai Package Manager 

The Bonsai package manager can be accessed from Bonsai's landing window or its workflow editor:

![Package manager from splash page](../../images/bonsai-splash-page-package-manager-highlight.png){width=350px} or ![Package manager from editor](../../images/bonsai-editor-package-manager-highlight.png){width=425px}

### Install Packages

The following packages are required to run the workflows in this documentation:

* `OpenEphys.Onix1.Design`: An extension of the `OpenEphys.Onix1` library that includes graphical user interfaces (GUIs). Installing OpenEphys.Onix1.Design automatically installs `OpenEphys.Onix1` as a dependency.
* `Bonsai.StarterPack`: the "standard library" for Bonsai that contains tools that are used in almost every workflow.
* `OpenEphys.Commutator`: for controlling Open Ephys commutators.
* `OpenEphys.Sockets.Bonsai`: for establishing TCP Sockets (to stream data to the Open Ephys GUI, for example).

> [!TIP]
> Additional packages will allow you to extend the functionality of ONIX hardware beyond the scope
> of this documentation. There are packages that allow ONIX be combined with [visual
> psychophysics](https://bonsai-rx.org/docs/tutorials/vision-psychophysics.html), [marker-less pose
> estimation](https://bonsai-rx.org/sleap/), [HARP behavioral devices](https://harp-tech.org/), and
> much more.

To install packages, open the package manager and:

1.  Click the `Browse` tab.
1.  Set `Package source` to `All`.
1.  Search for the exact package name listed above, e.g. `OpenEphys.Onix1.Design`.
1.  Click `Install`.
1.  If a license agreement window appears, click `I Accept`.

![Bonsai OpenEphys.Onix1.Design Install Screenshot](../../images/bonsai-install-OpenEphys.Onix1.Design.webp){width=650px}

### Update Packages

It is good practice to periodically check for package updates. To do this, open the package manager and:

1.  Click the `Update` tab.
1.  Set `Package source` to `All`.
1.  Leave the search bar blank if you want to check for updates for all installed packages.\
    Alternatively, if you want to check for an update for a particular package, you may type that package's name in the search bar to expedite the update retrieval process.
1.  Click `Update All` if you want to perform all available updates that appear in the package browser.\
    Alternatively, click on a package and click `Update` if you want to perform a subset of the available updates.

![Bonsai Update All or Just One Screenshot](../../images/bonsai-update.webp){width=650px}

### Uninstall Packages

Sometimes it is helpful to uninstall packages. Open the package manager and:

1.  Click the `Installed` tab.
1.  Set `Package source` to `All`.
1.  Leave the search bar blank if you want to see all installed packages.\
    Alternatively, if you want to uninstall a particular package, you may type that package's name in the search bar.
1.  Click a package and click `Uninstall`.

![Bonsai Uninstall Screenshot](../../images/bonsai-uninstall-Bonsai.OpenEphys.webp){width=650px}

## Next Step

Now that Bonsai and pertinent packages are installed, the next step is to learn how to use the
workflow editor to place operators from these newly acquired packages into a workflow.
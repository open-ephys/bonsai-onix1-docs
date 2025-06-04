> [!IMPORTANT] 
> These docs (including this README.md) are a work-in-progress. If you run into any obstacles developing these docs, or if there is any obfuscated, inaccurate, or missing content, please raise awareness by submitting an issue. Thanks!

# Onix1 Bonsai Docs

Documentation for the [Onix1 Bonsai package](https://github.com/open-ephys/bonsai-onix1).

These docs are built using [docfx](https://dotnet.github.io/docfx/index.html).

## Initialize the local Onix1 Bonsai Repository for Building Locally

These actions only need to be performed once when setting up the repo locally.

Download and install [dotnet](https://dotnet.microsoft.com/en-us/download) if it is not installed already.

Download and install [git](https://git-scm.com/downloads) if it is not installed already.

> [!NOTE]  
> The `docfx` program provides very little feedback about its state on the command line.
> It often appears to hang because it does not output any status information.
> Usually, the command will eventually return.

1. Using Windows PowerShell or a Git Bash terminal, clone the documentation repository:
    ``` console
    git clone https://github.com/open-ephys/bonsai-onix1-docs
    cd bonsai-onix1-docs
    ```
1. Pull in the latest files from the submodules according to the commit that the submodules point to:
    ``` console
    git submodule update --recursive --init
    ```
    In particular, the source code is available in this repo as a submodule. This will update the source code to the latest commit on main.
1. Configure the docfx version and restore docfx companion tools such as [DocLinkChecker](https://github.com/Ellerbach/docfx-companion-tools/tree/main/src/DocLinkChecker). You need to be in the same root folder where you cloned the repository for this to work. Run:
    ``` console
    dotnet tool restore
    ```
    to make the `docfx` command available.
   
    If the above command yields the following error:
    ``` console
    It was not possible to find any installed .NET Core SDKs
    ```
    even after installing .NET as described previously in the readme, refer to [this comment](https://github.com/dotnet/core/issues/6095#issuecomment-809006602) for a potential fix. If you follow the instructions described in the comment, make sure you proceed in a terminal or command prompt opened after changing the environment variables.
1. Set up a local Bonsai environment for automatically exporting SVGs, run Setup.ps1 in PowerShell (or, if not using PowerShell, run Setup.Cmd): 
    ``` console
    cd .\src\bonsai-onix1\.bonsai\
    ./Setup.ps1
    ```
    If the above command yields the following error:
    ``` console
    ./Setup.ps1 : File C:\Users\User\...\bonsai-onix1-docs\Setup.ps1 cannot be loaded because running scripts is      
    disabled on this system. For more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170. 
    At line:1 char:1
    + ~~~~~~~~~~~
        + CategoryInfo          : SecurityError: (:) [], PSSecurityException
        + FullyQualifiedErrorId : UnauthorizedAccess
    ```
    Run a command like this `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned` in Windows Powershell as admin. You can modify the choose which [execution policy](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.4) best suits your needs. The scope of the execution policy can also be set using [Set-ExecutionPolicy](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-7.5). `RemoteSigned` is the most restrictive policy that allows running local powershell scripts without signing them.

## Build Documentation Locally

To build the docs and serve locally, run in PowerShell:

``` console
./build.ps1 --serve
```

If this doesn't run, see comment in section above.

If SVGs are already exported and do not need to be updated, they don't need to be re-exported. In that case, to build the docs and serve locally more quickly, run:

``` console
dotnet docfx --serve
```

## Update Submodules

It is best practice to develop docs with the submodule directories containing the latest commits in their respective `main` branches (unless you are intentionally testing local changes to or another branch of the source code, for example). To update all submodules, run:

``` console
git submodule update --recursive --remote
```

## Before Pushing

The following three commands are run remotely by remote GitHub Actions serve upon pushing to a branch. The branch will not be able to merge to main unless all three commands complete successfully without any errors. Confirm that they can complete successfully without errors locally before committing and pushing. Otherwise, the branch becomes cluttered with potentially several attempts to pass the link-check process. Run: 

``` console
.\build.ps1 --logLevel Suggestion --warningsAsErrors
dotnet DocLinkChecker -v -f .github/workflows/DocLinkChecker.config
```

If the above command fails because "you must install or update .NET", follow the URL from the failed command's output or [this one](https://dotnet.microsoft.com/en-us/download/dotnet/6.0/runtime?cid=getdotnetcore&os=windows&arch=x64) to download and install .NET runtime 6. Dotnet supports simultaneous installation of several .NET runtime versions, and version 6 is required to run the DocLinkChecker.

The above set of commands can also be run using the `docfx-utils.ps1` Powershell script. Specifically, run `./docfx-utils.ps1 -d` in the repo's root directory to run DocLinkChecker, and run `./docfx-utils.ps1 -b` to build the site. 

To run the next command, install [Lychee](https://github.com/lycheeverse/lychee?tab=readme-ov-file) by following [these instructions](https://github.com/lycheeverse/lychee?tab=readme-ov-file#installation). If you are use Windows and download a Lychee executable, amend the below command according to the location and version of your Lychee executable, and run it.

``` console
<lychee/installation/directory>/lychee-v<x.xx.x>-windows-x86_64.exe --no-progress --base _site --exclude ^https://github\.com.*merge.* --exclude ^https://github\.com.*apiSpec.* --exclude ^https://github\.com/open-ephys/onix1-bonsai-docs/blob/.*/#L1 '_site/**/*.html' --max-retries 0 --max-concurrency 32 --cache --max-cache-age 1d
```

If you use a different operating systems and a different methods of installation, the above command might require additional amendments. 

The above command can also be run using the `docfx-utils.ps1` Powershell script. Specifically, run `./docfx-utils.ps1 -l <path/to/lychee.exe>` in the repo's root directory. 

All three link-checking commands can be run with the following command: `./docfx-utils.ps1 -a` in the repo's root directory. This command additionally cleans remaining artifacts from past builds before performing all the link-checking commands. This is the most robust and expedient way to confirm that the repo will pass the link checks when pushed. 

### docfx-utils.ps1

This is summary of docfx-utils.ps1 list members. They are described above, but they are also described below for ease-of-finding:

- `docfx-utils.ps1 -c` cleans cached files/removes artifacts from previous builds.
- `docfx-utils.ps1 -b` exports SVGs and builds the docs.
- `docfx-utils.ps1 -d` check the markdown files for broken references using DocLinkChecker.
- `docfx-utils.ps1 -l <path/to/lychee.exe>` checks for broken/missing links and references using lychee.
- `docfx-utils.ps1 -a <path/to/lychee.exe>` performs all of the above steps.

`docfx-utils.ps1 -l` and `docfx-utils.ps1 -a` will not run without a path to a lychee executable.   

> [!NOTE]  
> The docfx-utils.ps1 script (.ps1 PowerShell scripts in general) must be run in PowerShell.

These commands do not serve the docs. Serve them by running `dotnet docfx serve _site`. Note that this will not work if the documentation website has not been previously built. If the SVGs have been created, but the `_site` folder is empty and the only option that needs to be run is building the documentation pages, run `dotnet docfx --serve` to build the pages and automatically serve them.

## `dotnet docfx`

Running `dotnet docfx` runs both the `dotnet docfx metadata` command and the `dotnet docfx build` command in that order. Unless specified otherwise, `dotnet docfx` uses the `docfx.json` as its config file.

### metadata

The metadata command generates a .yml files containing metadata from the source code. These files contain information about class members, class inheritance, enum fields, etc. and \<xml\> comments from the source code. The input files for the `metadata` command are specified in `metadata.src` of the `docfx.json` file, and the output directory of the `metadata` command is specified in `metadata.dest` of the `docfx.json` file. 

### build

The build command generates raw and view data models for each .yml file generated by the `metadata` command and uses those raw and view data models to populate a template with data. 

The build process involves multiple steps:

1. Generates a raw data model from each .yml file.
1. Uses template to generate view data model from the raw data model. To see the raw model, refer to the relevant command in the [Troubleshooting](#troubleshooting) section of this readme. 
1. Uses template to populate pages with data from the view data model. To see the view models, refer to the relevant command in the [Troubleshooting](#troubleshooting) section of this readme.

The user can hook into and modify the build process at each of these steps by editing the template. 

All of the files involved in defining the template are specified in the `build.template` of the `docfx.json` file. The order in which the templates are defined matters. If the templates contain files with conflicting names, the template specified later overrides the template specified earlier with its conflicting file(s). This is helpful because it enables building custom templates on top of other templates. To see the docfx `default` and `modern` templates, refer to the relevant command in the [Troubleshooting](#troubleshooting) section of this README.md. 

The input files for the `build` command are specified in `build.content` of the `docfx.json` file, and the output directory of the `build` command is specified in `build.output` of the `docfx.json` file. 

## Docfx Template System

The docfx template system comprises of two primary components: the `.js` preprocessor files and the `.tmpl` renderer files. The preprocessor files are used to transform the raw data model into a view data model. The renderer files are templates that use data from the view data model to populate pages. 

### [Preprocessor](https://dotnet.github.io/docfx/tutorial/intro_template.html#preprocessor)

There are two functions that are called during the preprocessor step. They are `getOptions()` and `transform()`. They are called for every .yml file generated by the `metadata` command. `getOptions()` provides the user with the opportunity to modify the raw data model. `transform()` provides the user with the opportunity to modify the view data model.

When `getOptions()` is called for a given .yml file, setting the `isShared` flag as `true` incorporates the raw data model for every other .yml file into the raw data model of the .yml file whose `isShared` flag as `true`. This provides access to other classes', enums', namespaces', etc. metadata when `transform()` is called. This flag greatly expands the possibilities so it's worth explicitly mentioning. Setting the `isShared` flag as `true` would correspond with hooking into step 1 of the [build](#build) process. 

The `transform()` function transforms the raw data model to the view data model. Through this transformation process, the user can add logic to the template and process the source code's metadata. The default `transform()` function can be overwritten by writing your own `transform()` function in `<xyz>.overwrite.js` or can be extended by writing your own `preTransform` and `postTransform` in the `<xyz>.extension.js` file. Extending or overwriting the `transform()` function would correspond with hooking into step 2 of the [build](#build) process. 

### [Renderer](https://dotnet.github.io/docfx/tutorial/intro_template.html#renderer)

The renderer step utilizes [mustache](http://mustache.github.io/) syntax to create a template which is populated with data from the view model data. Writing custom `.tmpl` files would correspond with hooking into step 3 of the [build](#build) process. 

## Troubleshooting

The template in this repo builds upon the `default` and `modern` templates built into docfx. It might be helpful to reference those templates. To view them, run:

``` console
dotnet docfx template export default modern
```

It might be helpful to view the intermediate data models involved in the build process. To view those models, build, and serve the docs locally, run:

``` console
dotnet docfx --exportRawModel --rawModelOutputFolder _raw --exportViewModel --viewModelOutputFolder _view --serve
```

Strip the `--serve` option and append `--dryRun` option if you want to export the models without completing the build process and serving.

If local html pages don't appear to be updating, hard refresh website pages in browser. `Ctrl+Shift+R` and `Ctrl+F5` are common hotkeys for hard refreshes. 

If there are discrepancies between local and remote builds:

* Confirm local and remote docfx versions are consistent. This inconsistency can occur when, for example, running `docfx` instead of `dotnet docfx` or running `dotnet tool restore --configfile <configfile>` on another config file other than the one in this repo.
* Clear any locally cached files that aren't available remotely. Such files exist in the `api` directory (though care to not delete the `.gitignore` in that directory), the `_site` directory, and the workflows directory. Run `./docfx-utils.ps1 -c` to clean artifacts from previous builds. 

## Style Guide

Refer to the [Style Guide](style-guide.md).

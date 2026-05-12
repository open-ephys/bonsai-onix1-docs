#Requires -Version 5.1
<#
.SYNOPSIS
Brings types from an external NuGet package into docfx's api/ directory.

.DESCRIPTION
Two-phase helper called from build.ps1 around `dotnet docfx metadata`:
  -Package <name>   stages the package DLL + XML + dependency DLLs into the
                    staging dir read by docfx's external metadata entry.
  -Types <uids>     after metadata has run, copies the named type YAMLs from
                    the external output dir into the main api/ dir.

All paths are read from docfx.json (or -DocfxConfig). The "external" metadata
entry is the one whose src.files glob matches *.dll; the "main" entry is the
one matching *.csproj. The csproj that references -Package supplies the
package version, target framework, and (by .NET SDK convention) the build
output directory used to resolve dependency DLLs.

.EXAMPLE
.\docfx-tools\Sync-ExternalApi.ps1 -Package Bonsai.System
dotnet docfx metadata
.\docfx-tools\Sync-ExternalApi.ps1 -Types 'Bonsai.IO.FileSink','Bonsai.IO.PathSuffix'
#>

[CmdletBinding()]
param(
    [string]$Package,
    [string[]]$Types,
    [string]$DocfxConfig = 'docfx.json'
)

$ErrorActionPreference = 'Stop'

if (($Package -and $Types) -or (-not $Package -and -not $Types)) {
    throw "Pass exactly one of -Package or -Types."
}

$cfg = Get-Content $DocfxConfig -Raw | ConvertFrom-Json
$mainMeta     = $cfg.metadata | Where-Object { $_.src[0].files[0] -like '*.csproj' } | Select-Object -First 1
$externalMeta = $cfg.metadata | Where-Object { $_.src[0].files[0] -like '*.dll'    } | Select-Object -First 1
if (-not $mainMeta -or -not $externalMeta) {
    throw "$DocfxConfig must have a metadata entry for csproj input and one for dll input."
}

$targetApiDir   = $mainMeta.dest
$externalApiDir = $externalMeta.dest
$stageDir       = $externalMeta.src[0].src

if ($Package) {
    # Find the csproj that references the package, and read its TFM + version.
    $csprojFile = $null
    $version = $null
    $tfm = $null
    foreach ($candidate in Get-ChildItem $mainMeta.src[0].files[0] -Recurse) {
        [xml]$xml = Get-Content $candidate
        $ref = $xml.Project.ItemGroup.PackageReference | Where-Object Include -eq $Package
        if ($ref) {
            $csprojFile = $candidate
            $version = $ref.Version
            $tfm = $xml.Project.PropertyGroup.TargetFramework | Where-Object { $_ } | Select-Object -First 1
            break
        }
    }
    if (-not $csprojFile) { throw "No csproj in '$($mainMeta.src[0].files[0])' references '$Package'." }

    # .NET SDK artifacts layout: <project_root>/artifacts/bin/<assembly>/<config>
    $depDir = Join-Path $csprojFile.Directory.Parent.FullName "artifacts\bin\$($csprojFile.BaseName)\release"

    $pkgLibDir = Join-Path $env:USERPROFILE ".nuget\packages\$($Package.ToLower())\$version\lib\$tfm"
    $pkgDll = Join-Path $pkgLibDir "$Package.dll"
    $pkgXml = Join-Path $pkgLibDir "$Package.xml"

    New-Item -ItemType Directory -Force -Path $stageDir | Out-Null
    Copy-Item $pkgDll $stageDir -Force
    if (Test-Path $pkgXml) { Copy-Item $pkgXml $stageDir -Force }

    # Stage any referenced assemblies that exist in the build output so docfx
    # can resolve them while reading the package.
    $asm = [Reflection.Assembly]::LoadFile((Resolve-Path $pkgDll))
    foreach ($ref in $asm.GetReferencedAssemblies()) {
        $depPath = Join-Path $depDir "$($ref.Name).dll"
        if (Test-Path $depPath) { Copy-Item $depPath $stageDir -Force }
    }
}
else {
    foreach ($t in $Types) {
        $src = Join-Path $externalApiDir "$t.yml"
        if (-not (Test-Path $src)) { throw "Expected YAML not produced: $src" }
        Copy-Item $src (Join-Path $targetApiDir "$t.yml") -Force
    }
}

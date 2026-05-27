# Build project
$libPath = ".\src\bonsai-onix1\"
dotnet build $libPath --configuration Release

# Export workflow vectors
$libPath = Join-Path $libPath "artifacts\bin\OpenEphys.Onix1\release"
.\docfx-tools\modules\Export-Image.ps1 -bootstrapperPath .\src\bonsai-onix1\.bonsai\Bonsai.exe $libPath

# Surface inherited Bonsai.IO.FileSink properties on FileSink-derived operators
$externalTypes = 'Bonsai.IO.FileSink', 'Bonsai.IO.PathSuffix'
.\include-external-api.ps1 -Package Bonsai.System
dotnet docfx metadata
.\include-external-api.ps1 -Types $externalTypes

dotnet docfx build @args

# External-type YAMLs exist only as data sources for the template extension;
# their generated HTML pages should not appear on our site.
.\include-external-api.ps1 -RemoveHtml -Types $externalTypes

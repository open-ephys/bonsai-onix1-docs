# Build project
$libPath = ".\src\bonsai-onix1\"
dotnet build $libPath --configuration Release

# Export workflow vectors
$libPath = Join-Path $libPath "artifacts\bin\OpenEphys.Onix1\release"
.\docfx-tools\modules\Export-Image.ps1 -bootstrapperPath .\src\bonsai-onix1\.bonsai\Bonsai.exe $libPath
dotnet docfx @args
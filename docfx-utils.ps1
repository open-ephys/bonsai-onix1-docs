[CmdletBinding(PositionalBinding=$false)]
param 
(
    [parameter(mandatory=$false)][switch][Alias("c")]$clean,
    [parameter(mandatory=$false)][switch][Alias("b")]$build,
    [parameter(mandatory=$false)][switch][Alias("d")]$doclinkchecker,
    [parameter(mandatory=$false)][string][Alias("l")]$linkcheck,
    [parameter(mandatory=$false)][string][Alias("a")]$all
)

# this is called removeartifacts instead of clean because clean might be already mean something in powershell?
function removeartifacts
{
    $deletePaths = ".\workflows\**\*.svg", ".\workflows\hardware\**\*.svg", ".\workflows\**\*.bonsai.layout", ".\workflows\hardware\**\*.bonsai.layout", ".\api\*.yml", ".\api\.manifest", ".\_site\", ".\_raw\", ".\_view\"

    foreach($deletePath in $deletePaths){if (Test-Path $deletePath){Remove-Item $deletePath -Recurse}}
    Write-Output ""
}

function build{.\build.ps1 --logLevel Suggestion --warningsAsErrors}

function linkcheck 
{
    param($lycheePath)
    Write-Output "`nRunning lychee..."
    Write-Output "------------------------------------------`n"
    Invoke-Expression "& `"$lycheePath`" --no-progress --base _site --exclude ^https://github\.com.*merge.* --exclude ^https://github\.com.*apiSpec.* '_site/**/*.html'"
    Write-Output "`n"
}

function doclinkchecker
{
    Write-Output "`nRunning DocLinkChecker..."
    Write-Output "------------------------------------------`n"
    dotnet DocLinkChecker -v -f .github/workflows/DocLinkChecker.config
}

if ($clean){removeartifacts}

if ($build){build}

if ($doclinkchecker){doclinkchecker}

if ($PSBoundParameters.ContainsKey("linkcheck")){linkcheck($linkcheck)}

if ($PSBoundParameters.ContainsKey("all"))
{
    Write-Output "`n------------------------------------------"
    Write-Output "Cleaning artifacts..."
    Write-Output "------------------------------------------"
    removeartifacts
    Write-Output "------------------------------------------"
    Write-Output "Exporting SVGs & building docs..."
    Write-Output "------------------------------------------`n"
    Start-Sleep -Seconds 2
    build
    Write-Output "`------------------------------------------"
    Write-Output "Running linkchecks..."
    Write-Output "------------------------------------------"
    Start-Sleep -Seconds 2
    doclinkchecker
    Start-Sleep -Seconds 2
    linkcheck($all)
}

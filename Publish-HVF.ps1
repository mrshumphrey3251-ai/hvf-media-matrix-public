param(
    [string]$Docket = "",
    [string]$Title = "",
    [string]$Body = "",
    [string]$BodyFile = "",
    [string]$Slug = "",
    [string]$Message = ""
)

$ErrorActionPreference = "Stop"
$RepoRoot = "C:\hvf_c2\hvf-media-matrix-private"
Set-Location $RepoRoot

$ArgsList = @("c2_cockpit\hvf_auto_publisher.py")
if ($Docket)   { $ArgsList += @("--docket", $Docket) }
if ($Title)    { $ArgsList += @("--title", $Title) }
if ($Slug)     { $ArgsList += @("--slug", $Slug) }
if ($Message)  { $ArgsList += @("--message", $Message) }

$TempBodyPath = ""
if ($Body) {
    $TempBodyPath = Join-Path $env:TEMP "hvf_publish_body_temp.txt"
    [System.IO.File]::WriteAllText($TempBodyPath, $Body, (New-Object System.Text.UTF8Encoding($false)))
    $ArgsList += @("--body-file", $TempBodyPath)
} elseif ($BodyFile) {
    $ArgsList += @("--body-file", $BodyFile)
}

try {
    & python @ArgsList
    if ($LASTEXITCODE -ne 0) {
        throw "hvf_auto_publisher.py exited with code $LASTEXITCODE"
    }
} finally {
    if ($TempBodyPath -and (Test-Path $TempBodyPath)) {
        Remove-Item $TempBodyPath -Force -ErrorAction SilentlyContinue
    }
}

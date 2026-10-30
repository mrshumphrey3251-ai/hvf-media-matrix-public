param(
    [string]$Docket = "",
    [string]$Title = "",
    [string]$Body = "",
    [string]$BodyFile = "",
    [string]$Message = ""
)

Set-Location "C:\hvf_c2\hvf-media-matrix-private"
$CmdArgs = @("c2_cockpit\hvf_auto_publisher.py")
if ($Docket)   { $CmdArgs += @("--docket", $Docket) }
if ($Title)    { $CmdArgs += @("--title", $Title) }
if ($Body)     { $CmdArgs += @("--body", $Body) }
if ($BodyFile) { $CmdArgs += @("--body-file", $BodyFile) }
if ($Message)  { $CmdArgs += @("--message", $Message) }

python @CmdArgs

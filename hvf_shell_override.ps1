$Host.UI.RawUI.WindowTitle = 'HVF Master Override & Zero-Trust Control'
Clear-Host
Write-Host "========================================================" -ForegroundColor DarkGray
Write-Host " HVF MASTER OVERRIDE & ZERO-TRUST CONTROL" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor DarkGray

$envPath = "C:\HVF_Repos\hvf-media-matrix-private\.env"
$validHash = ""
if (Test-Path $envPath) {
    $envLines = Get-Content $envPath
    foreach ($line in $envLines) { if ($line -match "^EBONY_AUTH_HASH=(.*)") { $validHash = $matches[1] } }
}

$SecureInput = Read-Host -Prompt "Enter Executive Passphrase to Authenticate" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureInput)
$PlainPass = [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($BSTR)
[System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR)

$Bytes = [System.Text.Encoding]::UTF8.GetBytes($PlainPass)
$Sha256 = [System.Security.Cryptography.SHA256]::Create()
$InputHash = [System.BitConverter]::ToString($Sha256.ComputeHash($Bytes)).Replace("-", "").ToLower()

if ($InputHash -ne $validHash) {
    Write-Host "
[!] ACCESS DENIED. INTRUSION ATTEMPT LOGGED." -ForegroundColor Red
    Start-Sleep -Seconds 2
    Exit
}

Write-Host "
[1] ENFORCE ZERO-TRUST (Lock side doors + Whitelist Only)"
Write-Host "[2] SUSPEND ZERO-TRUST (Maintenance Mode - Unrestricted Execution)"
$choice = Read-Host -Prompt "Select operational mode (1 or 2)"

$AppsToLock = @("cmd.exe", "powershell_ise.exe", "wt.exe", "pwsh.exe", "git-bash.exe", "wsl.exe", "mintty.exe")
$RunPolPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
$SaferPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\Safer\CodeIdentifiers"

if ($choice -eq '2') {
    foreach ($App in $AppsToLock) {
        $RegPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\$App"
        if (Test-Path $RegPath) { Remove-ItemProperty -Path $RegPath -Name "Debugger" -ErrorAction SilentlyContinue }
    }
    if (Test-Path $RunPolPath) { Remove-ItemProperty -Path $RunPolPath -Name "NoRun" -ErrorAction SilentlyContinue }
    if (Test-Path $SaferPath) { Set-ItemProperty -Path $SaferPath -Name "DefaultLevel" -Value 262144 -Type DWord -ErrorAction SilentlyContinue }
    Write-Host "
[+] System UNLOCKED. Zero-Trust suspended." -ForegroundColor Green
} else {
    $DebuggerString = "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Normal -File ""C:\HVF_Repos\hvf-media-matrix-private\hvf_shell_bouncer.ps1"""
    foreach ($App in $AppsToLock) {
        $RegPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\$App"
        if (-not (Test-Path $RegPath)) { New-Item -Path $RegPath -Force | Out-Null }
        Set-ItemProperty -Path $RegPath -Name "Debugger" -Value $DebuggerString -Force
    }
    if (-not (Test-Path $RunPolPath)) { New-Item -Path $RunPolPath -Force | Out-Null }
    Set-ItemProperty -Path $RunPolPath -Name "NoRun" -Value 1 -Type DWord -Force
    
    if (-not (Test-Path $SaferPath)) { New-Item -Path $SaferPath -Force | Out-Null }
    Set-ItemProperty -Path $SaferPath -Name "TransparentEnabled" -Value 1 -Type DWord -Force
    
    # Remove LNK (shortcuts) from strict executable blocking so taskbar icons still function
    $ExecTypes = @("WSC","VB","URL","SHS","SCR","REG","PIF","PCD","OCX","MST","MSP","MSI","MDT","MDA","ISP","INS","INF","HTA","HLP","EXE","CRT","CPL","COM","CMD","CHM","BAT","BAS","APP","ADP","ADE")
    Set-ItemProperty -Path $SaferPath -Name "ExecutableTypes" -Value $ExecTypes -Type MultiString -Force
    
    $UnrestrictedPath = "$SaferPath\262144\Paths"
    if (-not (Test-Path $UnrestrictedPath)) { New-Item -Path $UnrestrictedPath -Force | Out-Null }
    
    $SafeZones = @{
        "{11111111-1111-1111-1111-111111111111}" = "%WINDIR%"
        "{22222222-2222-2222-2222-222222222222}" = "%PROGRAMFILES%"
        "{33333333-3333-3333-3333-333333333333}" = "C:\HVF_Repos"
        "{44444444-4444-4444-4444-444444444444}" = "C:\Program Files (x86)"
        "{55555555-5555-5555-5555-555555555555}" = "$env:USERPROFILE\AppData\Local"
        "{66666666-6666-6666-6666-666666666666}" = "$env:USERPROFILE\AppData\Roaming"
    }
    
    foreach ($Zone in $SafeZones.GetEnumerator()) {
        $ZonePath = "$UnrestrictedPath\$($Zone.Name)"
        if (-not (Test-Path $ZonePath)) { New-Item -Path $ZonePath -Force | Out-Null }
        Set-ItemProperty -Path $ZonePath -Name "ItemData" -Value $Zone.Value -Force
    }
    
    Set-ItemProperty -Path $SaferPath -Name "DefaultLevel" -Value 0 -Type DWord -Force
    Write-Host "
[+] System LOCKED. Zero-Trust Whitelist Enforced." -ForegroundColor Green
}

Write-Host "[*] Restarting Windows Explorer to enforce perimeter..." -ForegroundColor Cyan
Start-Sleep -Seconds 2
Stop-Process -Name explorer -Force

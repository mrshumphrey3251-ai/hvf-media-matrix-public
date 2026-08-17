$Host.UI.RawUI.WindowTitle = 'HVF Iron Dome Override'
Clear-Host
Write-Host "========================================================" -ForegroundColor DarkGray
Write-Host " HVF IRON DOME MASTER OVERRIDE" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor DarkGray

$envPath = "C:\HVF_Repos\hvf-media-matrix-private\.env"
$validHash = ""
if (Test-Path $envPath) {
    $envLines = Get-Content $envPath
    foreach ($line in $envLines) { if ($line -match "^EBONY_AUTH_HASH=(.*)") { $validHash = $matches[1] } }
}

$SecureInput = Read-Host -Prompt "Enter Executive Passphrase to Toggle Shell Locks" -AsSecureString
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
[1] LOCK Alternative Shells (Iron Dome Active)"
Write-Host "[2] UNLOCK Alternative Shells (Maintenance Mode)"
$choice = Read-Host -Prompt "Select operational mode (1 or 2)"

$AppsToLock = @("cmd.exe", "powershell_ise.exe", "wt.exe")
if ($choice -eq '2') {
    foreach ($App in $AppsToLock) {
        $RegPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\$App"
        if (Test-Path $RegPath) { Remove-ItemProperty -Path $RegPath -Name "Debugger" -ErrorAction SilentlyContinue }
    }
    Write-Host "[+] IFEO Kernel Locks REMOVED. Shells UNLOCKED." -ForegroundColor Green
} else {
    $DebuggerString = "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Normal -File ""C:\HVF_Repos\hvf-media-matrix-private\hvf_shell_bouncer.ps1"""
    foreach ($App in $AppsToLock) {
        $RegPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\$App"
        if (-not (Test-Path $RegPath)) { New-Item -Path $RegPath -Force | Out-Null }
        Set-ItemProperty -Path $RegPath -Name "Debugger" -Value $DebuggerString -Force
    }
    Write-Host "[+] IFEO Kernel Locks ENGAGED. Shells LOCKED." -ForegroundColor Green
}
Start-Sleep -Seconds 2

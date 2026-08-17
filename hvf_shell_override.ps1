$Host.UI.RawUI.WindowTitle = 'HVF Iron Dome Override'
Clear-Host
Write-Host "========================================================" -ForegroundColor DarkGray
Write-Host " HVF IRON DOME MASTER OVERRIDE" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor DarkGray

$envPath = "C:\HVF_Repos\hvf-media-matrix-private\.env"
$validHash = ""
if (Test-Path $envPath) {
    $envLines = Get-Content $envPath
    foreach ($line in $envLines) {
        if ($line -match "^EBONY_AUTH_HASH=(.*)") { $validHash = $matches[1] }
    }
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

if ($choice -eq '2') {
    Remove-ItemProperty -Path "HKCU:\Software\Policies\Microsoft\Windows\System" -Name "DisableCMD" -ErrorAction SilentlyContinue
    Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" -Name "DisallowRun" -ErrorAction SilentlyContinue
    Write-Host "[+] Shells UNLOCKED. Restarting Windows Explorer..." -ForegroundColor Green
} else {
    Set-ItemProperty -Path "HKCU:\Software\Policies\Microsoft\Windows\System" -Name "DisableCMD" -Value 2 -Type DWord -Force
    $expPolPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
    if (-not (Test-Path $expPolPath)) { New-Item -Path $expPolPath -Force | Out-Null }
    Set-ItemProperty -Path $expPolPath -Name "DisallowRun" -Value 1 -Type DWord -Force
    $disallowPath = "$expPolPath\DisallowRun"
    if (-not (Test-Path $disallowPath)) { New-Item -Path $disallowPath -Force | Out-Null }
    Set-ItemProperty -Path $disallowPath -Name "1" -Value "powershell_ise.exe" -Type String -Force
    Set-ItemProperty -Path $disallowPath -Name "2" -Value "wt.exe" -Type String -Force
    Set-ItemProperty -Path $disallowPath -Name "3" -Value "pwsh.exe" -Type String -Force
    Write-Host "[+] Shells LOCKED. Restarting Windows Explorer..." -ForegroundColor Green
}

Stop-Process -Name explorer -Force

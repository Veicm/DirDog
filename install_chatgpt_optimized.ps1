# -------------------------------
# Admin-Abfrage
# -------------------------------
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Skript benötigt Administratorrechte. Starte neu..."
    $args = "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    Start-Process powershell -Verb RunAs -ArgumentList $args
    exit
}
Write-Host "Skript läuft mit Administratorrechten!"

# -------------------------------
# Variablen
# -------------------------------
$repoOwner = "Veicm"
$repoName = "DirDog"
$zipName = "DirDog.zip"
$tempDir = "$env:TEMP\DirDogInstall"
$appDataDir = "$env:APPDATA\DirDog"
$programsDir = "C:\Program Files\DirDog"

# -------------------------------
# Temp bereinigen
# -------------------------------
if (Test-Path $tempDir) { cmd /c "rmdir /s /q `"$tempDir`"" }
New-Item -ItemType Directory -Path $tempDir | Out-Null

# -------------------------------
# GitHub Release holen
# -------------------------------
$apiUrl = "https://api.github.com/repos/$repoOwner/$repoName/releases/latest"
$release = Invoke-RestMethod -Uri $apiUrl -Headers @{ "User-Agent" = "PowerShell" }

$asset = $release.assets | Where-Object { $_.name -eq $zipName }
if (-not $asset) { Write-Error "DirDog.zip nicht gefunden"; exit }

# -------------------------------
# Schnell herunterladen
# -------------------------------
$zipPath = Join-Path $tempDir $zipName
Write-Host "Lade $zipName herunter..."
Start-BitsTransfer -Source $asset.browser_download_url -Destination $zipPath

# -------------------------------
# Schnell entpacken
# -------------------------------
Write-Host "Entpacke $zipName..."
$sevenZip = "C:\Program Files\7-Zip\7z.exe"
if (Test-Path $sevenZip) {
    & $sevenZip x $zipPath -o$tempDir -y | Out-Null
} else {
    Expand-Archive -Path $zipPath -DestinationPath $tempDir -Force
}

# -------------------------------
# Programmordner erstellen & verschieben
# -------------------------------
if (-not (Test-Path $programsDir)) { New-Item -ItemType Directory -Path $programsDir | Out-Null }
Get-ChildItem -Path $tempDir -Directory | ForEach-Object {
    $dest = Join-Path $programsDir $_.Name
    if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
    Move-Item -Path $_.FullName -Destination $dest
}

# -------------------------------
# Shortcut auf Desktop & Startmenü
# -------------------------------
$mainProgram = Join-Path $programsDir "Frondend_exe\__main__.exe"
$desktopShortcut = "$env:USERPROFILE\Desktop\DirDog1.lnk"
$startMenuShortcut = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\DirDog.lnk"

foreach ($shortcutPath in @($desktopShortcut, $startMenuShortcut)) {
    $WshShell = New-Object -ComObject WScript.Shell
    $shortcut = $WshShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $mainProgram
    $shortcut.WorkingDirectory = Split-Path $mainProgram
    $shortcut.Save()
}

# -------------------------------
# APPDATA verschieben
# -------------------------------
$sourceAppFolder = Join-Path $programsDir "Program1\_internal"
if (Test-Path $sourceAppFolder) {
    if (-not (Test-Path $appDataDir)) { New-Item -ItemType Directory -Path $appDataDir | Out-Null }
    Move-Item -Path $sourceAppFolder -Destination $appDataDir -Force
}

# -------------------------------
# Temp bereinigen
# -------------------------------
cmd /c "rmdir /s /q `"$tempDir`""

Write-Output "DirDog Installation abgeschlossen!"

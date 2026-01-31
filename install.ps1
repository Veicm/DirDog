
# Install DirDog from latest release of Veicm/DirDog

# Set variables
$repoOwner = "Veicm"
$repoName = "DirDog"
$zipName = "DirDog.zip"
$tempDir = "$env:TEMP\DirDogInstall"
$appDataDir = "$env:APPDATA\DirDog"
$programsDir = "C:\Program Files\DirDog"

# Clean up previous temp
if (Test-Path $tempDir) { Remove-Item -Recurse -Force $tempDir }
New-Item -ItemType Directory -Path $tempDir | Out-Null

# Get latest release info from GitHub API
$apiUrl = "https://api.github.com/repos/$repoOwner/$repoName/releases/latest"
$release = Invoke-RestMethod -Uri $apiUrl -Headers @{ "User-Agent" = "PowerShell" }

# Find DirDog.zip asset
$asset = $release.assets | Where-Object { $_.name -eq $zipName }
if (-not $asset) {
    Write-Error "DirDog.zip not found in the latest release."
    exit
}

# Download the zip
$zipPath = Join-Path $tempDir $zipName
Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $zipPath

# Extract the zip
Expand-Archive -Path $zipPath -DestinationPath $tempDir -Force

# Create programs folder
if (-not (Test-Path $programsDir)) { New-Item -ItemType Directory -Path $programsDir | Out-Null }

# Move the three program folders
Get-ChildItem -Path $tempDir -Directory | ForEach-Object {
    $progName = $_.Name
    $dest = Join-Path $programsDir $progName
    if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
    Move-Item -Path $_.FullName -Destination $dest
}

# Make one program manually startbar (create shortcut on Desktop)
$mainProgram = Join-Path $programsDir "Frondend_exe\__main__.exe"  # passe "Program1" ggf. an den Ordnernamen an
$desktopShortcut = "$env:USERPROFILE\Desktop\DirDog1.lnk"
$WshShell = New-Object -ComObject WScript.Shell
$shortcut = $WshShell.CreateShortcut($desktopShortcut)
$shortcut.TargetPath = $mainProgram
$shortcut.WorkingDirectory = Split-Path $mainProgram
$shortcut.Save()

# Move specific folder contents to APPDATA
$sourceAppFolder = Join-Path $programsDir "Program1\_internal"  # passe ggf. den Ordnernamen an
if (Test-Path $sourceAppFolder) {
    if (-not (Test-Path $appDataDir)) { New-Item -ItemType Directory -Path $appDataDir | Out-Null }
    Get-ChildItem -Path $sourceAppFolder -Recurse | ForEach-Object {
        $destPath = $_.FullName.Replace($sourceAppFolder, $appDataDir)
        $destDir = Split-Path $destPath
        if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir | Out-Null }
        Move-Item -Path $_.FullName -Destination $destPath -Force
    }
}

# Cleanup temp
Remove-Item -Recurse -Force $tempDir

Write-Output "DirDog installation complete!"

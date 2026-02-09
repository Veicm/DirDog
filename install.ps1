
# DirDog Installer ??? CLEAN / GEH??RTET / LIVE LOGGING

# Vor Backup/Installation
try {
    $ExePath = "$ProgramDir\Frontend_exe_v2\__main__.exe"
    $proc = Get-Process | Where-Object { $_.Path -eq $ExePath } -ErrorAction SilentlyContinue
    if ($proc) {
        Log "Beende laufende DirDog Prozesse..."
        $proc | ForEach-Object { 
            try { $_.Kill() } catch { Log "Fehler beim Beenden: $_" }
        }
        Start-Sleep -Seconds 2
    }
} catch {
    Log "FEHLER beim Pr??fen laufender Prozesse: $_"
}






$ErrorActionPreference = "Stop"

# -------------------------------
# Logging
# -------------------------------
$LogFile = "$env:TEMP\DirDog_install.log"

function Log {
    param([string]$Message)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] $Message"
    Write-Host $line
    Add-Content -Path $LogFile -Value $line
}

try {
    Log "===== INSTALLER START ====="

    # -------------------------------
    # Admin Check
    # -------------------------------
    $identity  = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($identity)

    if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        Write-Host "Keine Administratorrechte ??? Neustart als Administrator..."
        Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -NoExit -File `"$PSCommandPath`""
        exit
    }

    Write-Host "Administratorrechte best??tigt"

    # -------------------------------
    # Variablen
    # -------------------------------
    $RepoOwner   = "Veicm"
    $RepoName    = "DirDog"
    $ZipName     = "DirDog.zip"
    $TimeStamp   = Get-Date -Format "yyyyMMdd_HHmmss"

    $TempDir     = "$env:TEMP\DirDog_$TimeStamp"
    $ProgramDir  = "C:\Program Files\DirDog"
    $BackupDir   = "C:\Program Files\DirDog_BACKUP_$TimeStamp"
    $AppDataDir  = "$env:APPDATA\DirDog"

    Log "TempDir: $TempDir"

    # -------------------------------
    # Temp vorbereiten
    # -------------------------------
    try {
        New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
    } catch {
        Log "FEHLER beim Erstellen des Temp-Verzeichnisses: $_"
        throw
    }

    # -------------------------------
    # GitHub Release laden
    # -------------------------------
    try {
        Log "Hole GitHub Release Info"
        $ApiUrl  = "https://api.github.com/repos/$RepoOwner/$RepoName/releases/latest"
        $Release = Invoke-RestMethod -Uri $ApiUrl -Headers @{ "User-Agent" = "PowerShell" }

        $Asset = $Release.assets | Where-Object { $_.name -eq $ZipName }
        if (-not $Asset) {
            throw "DirDog.zip nicht gefunden im Release"
        }

        Log "Release Asset gefunden"
    } catch {
        Log "FEHLER beim Abrufen des GitHub Releases: $_"
        throw
    }

    # -------------------------------
    # Download (synchron, robust)
    # -------------------------------
    try {
        $ZipPath = "$TempDir\$ZipName"
        Log "Starte Download"

        $wc = New-Object System.Net.WebClient
        $wc.DownloadFile($Asset.browser_download_url, $ZipPath)

        Log "Download abgeschlossen"
    } catch {
        Log "FEHLER beim Download: $_"
        throw
    }

    # -------------------------------
    # Entpacken
    # -------------------------------
    try {
        Log "Entpacke ZIP"
        Expand-Archive -Path $ZipPath -DestinationPath $TempDir -Force
    } catch {
        Log "FEHLER beim Entpacken: $_"
        throw
    }

    # -------------------------------
    # Programme vorbereiten
    # -------------------------------
    try {
        if (Test-Path $ProgramDir) {
            Log "Sichere bestehende Installation"
            Rename-Item -Path $ProgramDir -NewName $BackupDir
        }

        Log "Installiere neue Version"
        New-Item -ItemType Directory -Path $ProgramDir -Force | Out-Null

        Get-ChildItem -Path $TempDir -Directory | Where-Object { $_.Name -ne "data" } | ForEach-Object {
    		Log "Kopiere Programmordner: $($_.Name)"
    		Copy-Item $_.FullName "$ProgramDir\$($_.Name)" -Recurse -Force
}

    } catch {
        Log "FEHLER beim Installieren der Programme: $_"
        throw
    }
# -------------------------------
# data ??? AppData (ZIP-root)
# -------------------------------
try {
    $DataSource = Join-Path $TempDir "data"

    if (-not (Test-Path $DataSource)) {
        throw "data Ordner nicht gefunden im ZIP: $DataSource"
    }

    Log "Verarbeite data Ordner: $DataSource"

    New-Item -ItemType Directory -Path $AppDataDir -Force | Out-Null

    Get-ChildItem -Path $DataSource | ForEach-Object {
        $Dest = Join-Path $AppDataDir $_.Name
        if (-not (Test-Path $Dest)) {
            Copy-Item $_.FullName $Dest -Recurse -Force
        } else {
            Log "  existiert: $($_.Name) (??bersprungen)"
        }
    }

} catch {
    Log "FEHLER beim Verarbeiten von data: $_"
    throw
}




    # -------------------------------
    # Desktop Shortcut
    # -------------------------------
    try {
        $ExePath = "$ProgramDir\Frontend_exe_v2\__main__.exe"
        if (Test-Path $ExePath) {
            Log "Erstelle Desktop Shortcut"
            $ShortcutPath = "$env:USERPROFILE\Desktop\DirDog.lnk"
            Remove-Item $ShortcutPath -ErrorAction SilentlyContinue

            $Shell = New-Object -ComObject WScript.Shell
            $SC = $Shell.CreateShortcut($ShortcutPath)
            $SC.TargetPath = $ExePath
            $SC.WorkingDirectory = Split-Path $ExePath
            $SC.Save()
        }
    } catch {
        Log "FEHLER beim Erstellen des Shortcuts: $_"
        throw
    }
# -------------------------------
# Autostart Shortcut
# -------------------------------
try {
    Log "Erstelle Verkn??pfung im Autostart"

    $ExePath = "C:\Program Files\DirDog\ParentDog_exe\ParentDog.exe"
    if (-not (Test-Path $ExePath)) {
        throw "Autostart-EXE nicht gefunden: $ExePath"
    }

    $LnkPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\DirDog.lnk"

    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($LnkPath)
    $Shortcut.TargetPath = $ExePath
    $Shortcut.WorkingDirectory = Split-Path $ExePath
    $Shortcut.Save()

    Log "Autostart-Verkn??pfung erfolgreich erstellt"
}
catch {
    Log "FEHLER beim Erstellen der Verkn??pfung im Autostart: $_"
}




Log "Erfolgreich die Verkn??pfung im Autostart erstellt"
    # -------------------------------
    # Cleanup
    # -------------------------------
    try {
        Log "Cleanup Temp"
        Remove-Item $TempDir -Recurse -Force
    } catch {
        Log "FEHLER beim Cleanup: $_"
    }

    Log "===== INSTALLATION ERFOLGREICH ====="
} catch {
    Log "`nINSTALLER ABGEBROCHEN! Fehler: $_"
}

Write-Host "`nDr??cke eine beliebige Taste zum Beenden..."
Read-Host

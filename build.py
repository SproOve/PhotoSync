import os
import shutil
import subprocess
import sys

# Name des Hauptskripts (anpassen, falls anders)
main_script = "PhotoSync.py"
config_file = "config.json"
dist_dir = "dist"

# Namen der benötigten ADB-Dateien
adb_files = [
    "adb/adb.exe",
    "adb/AdbWinApi.dll",
    "adb/AdbWinUsbApi.dll"
]

# Prüfen, ob alle ADB-Dateien vorhanden sind
missing = [f for f in adb_files if not os.path.isfile(f)]
if missing:
    print(f"Fehlende Dateien: {', '.join(missing)}")
    sys.exit(1)

# PyInstaller --add-data Argumente für alle Zusatzdateien
add_bin_args = []
for f in adb_files:
    add_data_args += ["--add-binary", f"{f};."]

# PyInstaller-Befehl
subprocess.run([
    "python",
    "-m",
    "PyInstaller",
    "--onefile",
    *add_bin_args,
    "--add-data", f"{config_file};.",
    main_script
], check=True)

# Zusatzdateien ins Ausgabeverzeichnis kopieren (überschreibt eingebettete Versionen)
exe_dir = os.path.join(dist_dir)
for f in adb_files + [config_file]:
    shutil.copy2(f, exe_dir)

print("Build abgeschlossen. Die ausführbare Datei, config.json und ADB-Dateien befinden sich in 'dist/'.")

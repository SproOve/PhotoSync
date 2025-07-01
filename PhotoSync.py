import os, json, shutil, time

import sys
import subprocess
from pathlib import Path
from datetime import datetime

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)


# Beispiel für Zugriff auf dest_path und valid_file_formats:
dest_path = config["dest_path"]
valid_formats = config["valid_file_formats"]

if os.path.exists(dest_path) == False:
    os.mkdir(dest_path)

#Standard Texts
txtRemoved = " wurde gelöscht"
txtUntagged = " wurde ungetagged"
txtSkipUndone = " wird übersprungen - Es sind noch nicht gelöschte Archive vorhanden"

def get_embedded_adb_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'adb')
    else:
        return os.path.join(os.path.dirname(__file__), 'adb')

def run_adb_command(cmd):
    adb_dir = get_embedded_adb_path()
    adb_exe = os.path.join(adb_dir, 'adb.exe')
    result = subprocess.run([adb_exe] + cmd, capture_output=True, text=True)
    return result.stdout.strip()

def ensure_folder_exists(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def get_file_modtime(path, type):
    if type == 'adb':
        try:
            # Android-Datei über ADB abfragen
            output = run_adb_command([
                'shell', 'stat', '-c', '%Y', f'"{path}"'
            ])
            timestamp = int(output.strip())
            return time.gmtime(timestamp)
        except Exception as e:
            print(f"⚠️ Fehler beim Android-Dateizugriff: {e}")
            return None
    elif type == 'local':
        try:
            # Lokale Datei (Windows)
            timestamp = os.path.getctime(path)
            return time.gmtime(timestamp)
        except Exception as e:
            print(f"⚠️ Fehler beim lokalen Dateizugriff: {e}")
            return None
    
# === HAUPTFUNKTIONEN ===

def list_android_files(folder):
    output = run_adb_command(['shell', 'ls', '-p', folder])
    files = [line.strip() for line in output.splitlines() if line and not line.endswith('/')]
    return files

def show_devices():
    print("🔌 Verbundene Geräte:")
    print(run_adb_command(['devices']))

def getQuartal(month):
    month = int(month)
    if  0 < month <= 3:
        quartal = 'Q1'
    elif 3 < month <= 6:
        quartal = 'Q2'
    elif 6 < month <= 9:
        quartal = 'Q3'
    elif 9 < month <= 12:
        quartal = 'Q4'
    return quartal
                

def check_file_format(file):
    validFileFormats = config["validFileFormats"]
    returnVal = False
    for fileFormat in validFileFormats:
        if file.lower().endswith(fileFormat):
            returnVal = True
    return returnVal

def pre_process_file(filepath, ob_type):
    changetime = get_file_modtime(filepath, ob_type)
    doSomething = check_file_format(filepath)
    if doSomething == True:
        quartal = getQuartal(changetime.tm_mon)
        destinationPath = dest_path + '\\' + str(changetime.tm_year) + '-' + quartal
        return destinationPath
    else:
        print(filepath + ' ist keine Mediendatei')
        return None

def process_file(filepath, dest_path, operation, type):
    if os.path.exists(dest_path) == False:
        os.mkdir(dest_path)
    print(f"{'📤 Kopiere' if operation == "copy" else '✂️  Verschiebe'}: {filepath}")
    if operation == 'copy':
        if type == 'adb':            
            run_adb_command(['pull', filepath, dest_path])
        elif type == 'local':
            shutil.copy2(filepath, dest_path)
    elif operation == 'move':
        if type == 'adb':            
            run_adb_command(['pull', filepath, dest_path])
            run_adb_command(['shell', 'rm', f'"{filepath}"'])
        elif type == 'local':
            shutil.move(filepath, dest_path) 

def workFolder(path_obj):
    path = path_obj["path"]
    operation = path_obj["mode"]
    if path_obj["type"] == 'adb':
        print('ADB-Modus erkannt')
        messenger = False
        print(f"📁 Zielordner: {dest_path}")
        ensure_folder_exists(dest_path)

        files = list_android_files(path)
        print(f"📄 Gefundene Dateien: {len(files)}")

        for filename in files:
            android_file = f"{path}/{filename}"
            dest_path = pre_process_file(android_file, path_obj["type"])
            if dest_path is not None:
                process_file(android_file, dest_path, operation, path_obj["type"])
    elif path_obj["type"] == 'local':
        print('Lokaler Modus erkannt')
        messenger = False
        for folders, subfolders, filenames in os.walk(path):
            for file in filenames:
                filepath = folders + '\\' + file
                dest_path = pre_process_file(filepath, path_obj["type"])
                if dest_path is not None:
                    process_file(filepath, dest_path, operation, path_obj["type"])


show_devices()
for path_obj in config["paths"]:
    workFolder(path_obj)
    print("✅ Vorgang abgeschlossen.")
enterPrompt = input("Zum Beenden Enter-Taste drücken...")



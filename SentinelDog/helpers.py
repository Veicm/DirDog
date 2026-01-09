import time
from pathlib import Path
import json
import hashlib
import threading
json_lock = threading.Lock()

with open('SentinelDog/check_changes_config.json', 'r', encoding='utf-8') as config_file:
    data = json.load(config_file)

def sha256_file(path, chunk_size=8192):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def push_change_files_into_api(path,type_of_action,new_path=None):
    global data

    parent_dir = str(Path(path).parent)
    extension = str(Path(path).suffix)
    file_name = str(Path(path).stem)
    # print("--------------------------------------------")
    # print(data["path"])
    # print("----")
    # print(path)


    # print("-------------------------------------------------")
    if str(parent_dir) !=str(data["path"]):
        print("Eintrag wurde übersprungen da die Datei in einem Unterordner liegt!")
        return

    if type_of_action == "Deleted":
        hashed_file = None
    else:
        try:
            hashed_file = str(sha256_file(new_path if new_path else path))    
        except (FileNotFoundError, PermissionError):
            hashed_file = None
            print("Eintrag wurde übersprungen da ein Ordner betroffen war !")
            return

    # print(extension)
    # print(file_name)

    print(path)
    changed_file = {
        "parent_dir": parent_dir,
        "file_name": file_name,
        "file_extension": extension,
        "new_path": new_path,
        "last_modified": int(time.time()),
        "SHA-256-Hash": hashed_file,
        "action": type_of_action


    }
    with json_lock:
        with open(data["api_file_path"], "r+", encoding="utf-8") as api_file:
            try:
                file_data = json.load(api_file)
            except json.JSONDecodeError:
                file_data = {"files": []}

            file_data.setdefault("files", []).append(changed_file)

            api_file.seek(0)
            json.dump(file_data, api_file, indent=2, ensure_ascii=False)
            api_file.truncate()
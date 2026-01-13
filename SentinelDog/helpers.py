import time
from pathlib import Path
import json
from multiprocessing.connection import Client
from py_essentials import hashing as hs
import threading

json_lock = threading.Lock()
with open("./check_changes_config.json", "r", encoding="utf-8") as config_file:
    data = json.load(config_file)
try:
    print("[+] Connection is prepared!")
    address = ("localhost", 6000)
    conn = Client(address, authkey=b"secret password")
    print("[+] Connection succesfull!")
except:
    print("[!] Error: Connecetion failed!")


def sha256_file(path):

    hash = hs.fileChecksum(path, "sha256")
    return str(hash)


def push_change_files_into_api(path, type_of_action, new_path=None):
    global data
    global conn
    parent_dir = str(Path(path).parent)
    extension = str(Path(path).suffix)
    file_name = str(Path(path).stem)

    try:
        new_name = str(Path(new_path).stem) + str(Path(new_path).suffix)
        new_file_extension = str(Path(new_path).suffix)
    except:
        new_file_extension = None
        new_name = None
        print("Error beim auswerten des neuen Pfades. (Normal bei 3/4 operationen)")

    print("--------------------------------------------")
    print(data["path"])
    print("----")
    print(parent_dir)

    print(str(Path(data["path"]).parent.resolve(strict=True)))
    print("------")
    print(Path(parent_dir).resolve(strict=True))
    print(Path(data["path"]).resolve(strict=True))

    print("-------------------------------------------------")
    if Path(parent_dir).resolve(strict=True) != Path(data["path"]).resolve(strict=True):
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
        "new_name": new_name,
        "new_file_extension": new_file_extension,
        "last_modified": int(time.time()),
        "SHA-256-Hash": hashed_file,
        "action": type_of_action,
    }
    conn.send(changed_file)

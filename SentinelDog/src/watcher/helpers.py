import time
from pathlib import Path
import json
from ipc.ipc import connect_to_host,send_data
from py_essentials import hashing as hs
import threading



def sha256_file(path):

    hash = hs.fileChecksum(path, "sha256")
    return str(hash)


def push_change_files_into_api(connection,path, type_of_action, checked_path,new_path=None):


    parent_dir = str(Path(path).parent)
    extension = str(Path(path).suffix)
    file_name = str(Path(path).stem)

    try:
        new_name = str(Path(new_path).stem) 
        new_file_extension = str(Path(new_path).suffix)
    except:
        new_file_extension = None
        new_name = None
        print("Error beim auswerten des neuen Pfades. Nur relevant beim umbennen!!")

    print("--------------------------------------------")

    print(f"New path: {str(Path(parent_dir).resolve())}")
    print(f"Old Path: {str(Path(path).resolve())}")

    print("-------------------------------------------------")
    if str(Path(parent_dir).resolve()) != str(Path(checked_path).resolve()):
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
    send_data(conn=connection,data=changed_file)

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
import time
import os
from pathlib import Path
import hashlib
import threading
json_lock = threading.Lock()

def sha256_file(path, chunk_size=8192):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()




with open('SentinelDog/check_changes_config.json', 'r', encoding='utf-8') as config_file:
    data = json.load(config_file)




def push_change_files_into_api(path,type_of_action,new_path=None):
    global data

    parent_dir = str(Path(path).parent)
    extension = str(Path(path).suffix)
    file_name = str(Path(path).stem)
    if type_of_action == "Deleted":
        hashed_file = None
    else:
        try:
            hashed_file = str(sha256_file(new_path if new_path else path))
        except (FileNotFoundError, PermissionError):
            hashed_file = None


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




class Handler(FileSystemEventHandler):
    def __init__(self):
        self.lock = False
        super().__init__()

    def on_moved(self, event):
        self.lock = True
        
        old_path = str(Path(event.src_path).resolve())
        new_path = str(Path(event.dest_path).resolve())

        print("Umbenannt:")
        print("ALT:", old_path)
        print("NEU:", new_path)
        push_change_files_into_api(str(Path(event.src_path).resolve()),"Renamed",str(Path(event.dest_path).resolve()))


    def on_modified(self, event):
        if not self.lock:
            print("Geändert:", event.src_path)
            push_change_files_into_api(str(Path(event.src_path).resolve()),"Changed")
        else:
            self.lock = False


    def on_created(self, event):
        print("Neu:", event.src_path)
        push_change_files_into_api(str(Path(event.src_path).resolve()),"Created")


    def on_deleted(self, event):
        print("Gelöscht:", event.src_path)
        push_change_files_into_api(str(Path(event.src_path).resolve()),"Deleted")




observer = Observer()
observer.schedule(Handler(), path=data["path"], recursive=True)
observer.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()

observer.join()

from watchdog.observers import Observer
from watcher.Handler_class import Handler
import threading
import json
from ipc.ipc import connect_to_host


def main(path):
    json_lock = threading.Lock()
    with open(
        r"../../DirDog/src/data/data_storage.json", "r", encoding="utf-8"
    ) as config_file:
        data = json.load(config_file)

    conn = connect_to_host()
    observer = Observer()
    observer.schedule(Handler(connection=conn), path=path, recursive=True)
    observer.start()

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

    observer.join()

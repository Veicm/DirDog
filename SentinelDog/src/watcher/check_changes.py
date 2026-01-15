from watchdog.observers import Observer
import json
import threading
from Handler_class import Handler


def main():
    json_lock = threading.Lock()


    with open("./check_changes_config.json", "r", encoding="utf-8") as config_file:
        data = json.load(config_file)


    observer = Observer()
    observer.schedule(Handler(), path=data["path"], recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()



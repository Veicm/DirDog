from watchdog.observers.polling import PollingObserver as Observer


from watcher.Handler_class import Handler
import threading
import json
from ipc.ipc import connect_to_host
import os

def main(path):



    conn = connect_to_host()
    observer = Observer()
    observer.schedule(Handler(connection=conn,path=path), path=path, recursive=True)
    observer.start()

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

    observer.join()

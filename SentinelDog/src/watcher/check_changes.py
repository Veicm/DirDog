from watchdog.observers import Observer
from watcher.Handler_class import Handler


def main(path):

    observer = Observer()
    observer.schedule(Handler(), path=path, recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()



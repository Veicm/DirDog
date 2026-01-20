from pathlib import Path
import threading
from watcher.helpers import *
from watchdog.events import FileSystemEventHandler
json_lock = threading.Lock()

# Darf nur auf Datein Prüfen und ordner auslassen!!!!
# Noch ist dies nicht gewährleistet.
# Nach dem Hash nach Null Filtern um Ordner auszuschließen
# Ausnahme bei "Deleted" dort darf Null nicht als ausnahme Zählen

# Und zusätzlich parent_dir mit angegebenen, zu überwachenden Pfad abgleicehn damit alle Dateien in Unterorndern ausgeschlossen werde.
#   /\
#   |
#   |  Fixxed/Implemented all
class Handler(FileSystemEventHandler):
    def __init__(self, path):
        self.lock = False
        self.path = path
        super().__init__()

    def on_moved(self, event):
        self.lock = True
        print("Neuer Eintrag wird erstellt! ---------------------------")
        old_path = str(Path(event.src_path).resolve())
        new_path = str(Path(event.dest_path).resolve())

        print("Umbenannt:")
        print("ALT:", old_path)
        print("NEU:", new_path)
        push_change_files_into_api(str(Path(event.src_path).resolve()),"Renamed",str(Path(event.dest_path).resolve()))


    def on_modified(self, event):
        print("Neuer Eintrag wird erstellt! ---------------------------")
        if not self.lock:
            print("Geändert:", event.src_path)
            push_change_files_into_api(str(Path(event.src_path).resolve()),"Changed")
        else:
            self.lock = False


    def on_created(self, event):
        print("Neuer Eintrag wird erstellt! ---------------------------")
        print("Neu:", event.src_path)
        push_change_files_into_api(str(Path(event.src_path).resolve()),"Created")


    def on_deleted(self, event):
        print("Neuer Eintrag wird erstellt! ---------------------------")
        print("Gelöscht:", event.src_path)
        push_change_files_into_api(str(Path(event.src_path).resolve()),"Deleted")
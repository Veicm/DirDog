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
    def __init__(self, path,connection):
        self.lock = False
        self.path = path
        self.conn=connection
        super().__init__()

    def on_moved(self, event):
        self.lock = True
        print("Neuer Eintrag wird erstellt! ---------------------------")
        old_path = str(Path(event.src_path).resolve())
        new_path = str(Path(event.dest_path).resolve())

        print("Umbenannt:")
        print("ALT:", old_path)
        print("NEU:", new_path)

        push_change_files_into_api(
            path=str(Path(event.src_path).resolve()),
            type_of_action="Renamed",
            connection=self.conn,
            new_path=new_path,
            checked_path = self.path
        )

    def on_modified(self, event):
        print("Neuer Eintrag wird erstellt! ---------------------------")
        if not self.lock:
            print("Geändert:", event.src_path)

            push_change_files_into_api(
            path=str(Path(event.src_path).resolve()),
            type_of_action="Changed",
            connection=self.conn,
            checked_path = self.path
        )

        else:
            self.lock = False


    def on_created(self, event):
        print("Neuer Eintrag wird erstellt! ---------------------------")
        print("Neu:", event.src_path)
        push_change_files_into_api(
            path=str(Path(event.src_path).resolve()),
            type_of_action="Created",
            connection=self.conn,
            checked_path = self.path
        )



    def on_deleted(self, event):
        print("Neuer Eintrag wird erstellt! ---------------------------")
        print("Gelöscht:", event.src_path)

        push_change_files_into_api(
            path=str(Path(event.src_path).resolve()),
            type_of_action="Deleted",
            connection=self.conn,
            checked_path = self.path
        )
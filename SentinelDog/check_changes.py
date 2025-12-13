from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

with open('check_changes_config.json', 'r', encoding='utf-8') as config_file:
    data = json.load(config_file)




def push_change_files_into_api(path,type_of_action):
    changed_file = {
        "path":path,
        "type":type_of_action

    }
    with open('api.json','r+',encoding="utf-8") as api_file:
        file_data = json.load(api_file)

        file_data["files"].append(changed_file)
        api_file.seek(0)
        json.dump(file_data,api_file)
        api_file.truncate()




class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        print("Geändert:", event.src_path)
        push_change_files_into_api(event.src_path,"Changed")
    def on_created(self, event):
        print("Neu:", event.src_path)
        push_change_files_into_api(event.src_path,"Created")
    def on_deleted(self, event):
        print("Gelöscht:", event.src_path)
        push_change_files_into_api(event.src_path,"Deleted")



observer = Observer()
observer.schedule(Handler(), path=data["path"], recursive=True)
observer.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()

observer.join()

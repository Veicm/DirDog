from watcher.check_changes import main
import json
from concurrent.futures import ThreadPoolExecutor
if __name__ == "__main__":

    with open(r"../../DirDog/src/data/data_storage.json", "r", encoding="utf-8") as config_file:
        data = json.load(config_file)
    paths=data["monitoring_dirs"]

    with ThreadPoolExecutor(max_workers=len(paths)) as executor:
        executor.map(main,paths)
from watcher.check_changes import main
import json
from concurrent.futures import ThreadPoolExecutor
if __name__ == "__main__":

    with open("config/check_changes_config.json", "r", encoding="utf-8") as config_file:
        data = json.load(config_file)
    paths=data["paths"]

    with ThreadPoolExecutor(max_workers=len(paths)) as executor:
        executor.map(main,paths)
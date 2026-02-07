from watcher.check_changes import main as single_main
import json
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path


def main() -> None:
    os.chmod(os.getenv("APPDATA") + r"\DirDog", 0o666)

    config_path = os.getenv("APPDATA") + r"\DirDog\config\data_storage.json"
    with open(str(Path(config_path).resolve()), "r", encoding="utf-8") as config_file:
        data = json.load(config_file)
    paths = data["monitoring_dirs"]

    with ThreadPoolExecutor(max_workers=len(paths)) as executor:
        futures = [executor.submit(single_main, path) for path in paths]
        for f in futures:
            f.result()  # blockiert dauerhaft


if __name__ == "__main__":
    main()

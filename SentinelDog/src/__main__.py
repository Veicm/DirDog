from watcher.check_changes import main as single_main
import json
from concurrent.futures import ThreadPoolExecutor


def main() -> None:
    with open(
        r"../../DirDog/src/data/data_storage.json", "r", encoding="utf-8"
    ) as config_file:
        data = json.load(config_file)
    paths = data["monitoring_dirs"]

    with ThreadPoolExecutor(max_workers=len(paths)) as executor:
        futures = [executor.submit(single_main, path) for path in paths]
        for f in futures:
            f.result()   # blockiert dauerhaft



if __name__ == "__main__":
    main()

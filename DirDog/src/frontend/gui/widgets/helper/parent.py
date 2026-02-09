import os
import json
import psutil
import subprocess
import time


class Parent:
    """Supervises and manages the HandlerDog and SentinelDog sub-programs.

    This class monitors both processes and restarts them if one or both
    are no longer running. It communicates with the DirDog frontend by
    observing configuration changes stored in a JSON file.
    """

    def __init__(self) -> None:
        """Initialize process names, configuration paths, and executables."""
        self.handler_dog_process_name: str = "HandlerDog.exe"
        self.sentinel_dog_process_name: str = "SentinelDog.exe"
        self.config_file_path: str = (
            str(os.getenv("APPDATA")) + r"\DirDog\config\data_storage.json"
        )
        self.handler_dog_exe_path: str = os.path.join(
            str(os.environ.get("ProgramFiles")),
            "DirDog",
            "HandlerDog_exe",
            "HandlerDog.exe",
        )
        self.sentinel_dog_exe_path: str = os.path.join(
            str(os.environ.get("ProgramFiles")),
            "DirDog",
            "SentinelDog_exe",
            "SentinelDog.exe",
        )

    def watch(self) -> None:
        """Continuously monitor both sub-programs.

        Runs an infinite loop that checks whether both processes are active.
        If one or both are not running, they are restarted. The check
        interval is 15 seconds.
        """
        while True:
            if self._is_auto_start() and not self._both_are_running():
                self.restart()
            time.sleep(15)

    def restart(self) -> None:
        """Restart both sub-programs.

        Terminates all running instances of HandlerDog and SentinelDog
        and starts fresh ones.
        """
        self._kill_both()
        self._start_both()

    def _is_auto_start(self) -> bool:
        """
        Check if auto-start is enabled in the configuration file.

        Reads the JSON configuration file and returns the value associated
        with the "auto_start" key. Defaults to True if the key is not present.

        Returns:
            bool: True if auto-start is enabled, False otherwise.
        """
        with open(self.config_file_path, "r", encoding="utf-8") as file:
            data: dict[str, bool | list[str]] = json.load(file)
        return bool(data.get("auto_start", True))

    def _both_are_running(self) -> bool:
        """Check whether both sub-programs are currently running.

        Returns:
            bool: True if both HandlerDog and SentinelDog processes are
            found, False otherwise.
        """
        with open(self.config_file_path, "r", encoding="utf-8") as file:
            data: dict[str, bool | list[str]] = json.load(file)

        for proc in psutil.process_iter():
            if self.handler_dog_process_name == proc.name():
                data["is_running_handler"] = True
                for proc in psutil.process_iter():
                    if self.sentinel_dog_process_name == proc.name():
                        data["is_running_sentinel"] = True
                        with open(self.config_file_path, "w", encoding="utf-8") as file:
                            json.dump(data, file, indent=4)
                        return True
                data["is_running_sentinel"] = False
                with open(self.config_file_path, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4)
                return False
        data["is_running_handler"] = False
        data["is_running_sentinel"] = False
        with open(self.config_file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        return False

    def _start_both(self) -> None:
        """Launch both sub-program executables."""
        subprocess.Popen([self.handler_dog_exe_path])
        subprocess.Popen([self.sentinel_dog_exe_path])

    def _kill_both(self) -> None:
        """Terminate all running HandlerDog and SentinelDog processes."""
        for proc in psutil.process_iter():
            if (
                self.handler_dog_process_name == proc.name()
                or self.sentinel_dog_process_name == proc.name()
            ):
                proc.kill()


def main() -> None:
    parent = Parent()
    parent.watch()


if __name__ == "__main__":
    main()

import os
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
        self.handler_dog_process_name: str = (
            "HandlerDog"  # TODO: change name when needed
        )
        self.sentinel_dog_process_name_name: str = (
            "SentinelDog"  # TODO: change name when needed
        )
        self.config_file_path: str = (
            str(os.getenv("APPDATA")) + r"\DirDog\config\data_storage.json"
        )
        self.handler_dog_exe_path: str = (
            r"C:\path\to\handler_dog.exe"  # TODO: change name when known
        )
        self.sentinel_dog_exe_path: str = (
            r"C:\path\to\sentinel_dog.exe"  # TODO: change name when known
        )

    def watch(self) -> None:
        """Continuously monitor both sub-programs.

        Runs an infinite loop that checks whether both processes are active.
        If one or both are not running, they are restarted. The check
        interval is 15 seconds.
        """
        while True:
            if not self._both_are_running():
                self.restart()
            time.sleep(15)

    def restart(self) -> None:
        """Restart both sub-programs.

        Terminates all running instances of HandlerDog and SentinelDog
        and starts fresh ones.
        """
        self._kill_both()
        self._start_both()

    def _both_are_running(self) -> bool:
        """Check whether both sub-programs are currently running.

        Returns:
            bool: True if both HandlerDog and SentinelDog processes are
            found, False otherwise.
        """
        for proc in psutil.process_iter():
            if self.handler_dog_process_name == proc.name():
                for proc in psutil.process_iter():
                    if self.handler_dog_process_name == proc.name():
                        return True
                return False
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
                or self.sentinel_dog_process_name_name == proc.name()
            ):
                proc.kill()

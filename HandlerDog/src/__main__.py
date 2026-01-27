from ipc.receiver import IPC
import os


def main() -> None:
    ipc = IPC(
        str(os.getenv("APPDATA")) + r"\demo.db",
        str(os.getenv("APPDATA")) + r"\demo_archive.db",
    )
    ipc.run_threading()


if __name__ == "__main__":
    main()

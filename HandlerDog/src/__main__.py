from ipc.receiver import IPC
import os


def main() -> None:
    ipc = IPC(
        os.path.join(os.getenv("APPDATA"), "DirDog", "demo.db"),
        os.path.join(os.getenv("APPDATA"), "DirDog", "demo_archive.db"),
    )
    ipc.run_threading()


if __name__ == "__main__":
    main()

from ipc.receiver import IPC


def main() -> None:
    ipc = IPC(r"./database/data/demo.db", r"./database/data/demo_archive.db")
    ipc.run_threading()


if __name__ == "__main__":
    main()

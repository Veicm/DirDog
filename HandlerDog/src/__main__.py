from ipc.receiver import IPC


def main() -> None:
    ipc = IPC(".\\database\\data\\demo.db", ".\\database\\data\\demo_archive.db")
    ipc.run_threading()


if __name__ == "__main__":
    main()

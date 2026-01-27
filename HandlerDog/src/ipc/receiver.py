from multiprocessing.connection import Connection, Listener
from threading import Thread
from typing import Any
from app_database.handler import Handler


class IPC:
    """Provide an IPC server that receives file events and forwards them to a handler."""

    def __init__(self, db_path: str, archive_path: str) -> None:
        """Initialize the IPC listener and accept an incoming connection.

        Args:
            db_path (str): Path to the main SQLite database.
            archive_path (str): Path to the archive SQLite database.
        """
        self.handler = Handler(db_path, archive_path)
        self.address = ("localhost", 6000)
        self.listener = Listener(self.address, authkey=b"secret password")

    def receive(self, connection) -> None:
        """Continuously receive and process incoming IPC messages.

        The method blocks on the connection and processes received data until a
        ``"close"`` message is received, at which point the connection and
        listener are shut down.

        Args:
            connection (Connection[Any, Any]): The connection, to use in this function.
        """
        while True:
            try:
                data: dict[str, str | int | None] | str = connection.recv()
            except EOFError:
                break

            if data == "close":
                break

            elif not isinstance(data, str):
                self.handler.process_data(data)

            else:
                raise ValueError(
                    f"{data} of type {type(data)} is not a valid content type for data_query."
                )
        connection.close()

    def run_threading(self) -> None:
        """receive data on multiple threads."""
        while True:
            connection: Connection[Any, Any] = self.listener.accept()
            print("connection successfull")
            thread = Thread(
                target=self.receive,
                args=(connection,),
                daemon=True,
            )
            thread.start()


def main() -> None:
    """Start the IPC server and begin receiving messages."""
    ipc = IPC(
        ".\\..\\database\\data\\demo.db", ".\\..\\database\\data\\demo_archive.db"
    )
    ipc.run_threading()


if __name__ == "__main__":
    main()

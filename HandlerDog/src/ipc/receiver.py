from multiprocessing.connection import Connection, Listener
from typing import Any
from database.handler import Handler


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
        self.connection: Connection[Any, Any] = self.listener.accept()
        print("connection accepted from", self.listener.last_accepted)

    def receive(self) -> None:
        """Continuously receive and process incoming IPC messages.

        The method blocks on the connection and processes received data until a
        ``"close"`` message is received, at which point the connection and
        listener are shut down.
        """
        while True:
            data_query: list[dict[str, str | int | None]] | str = self.connection.recv()
            if data_query == "close":
                self.connection.close()
                break
            elif not isinstance(data_query, str):
                self.handle_data(data_query)
            else:
                raise ValueError(
                    f"{data_query} of type {type(data_query)} is not a valid content type for data_query."
                )
        self.listener.close()

    def handle_data(self, data_query: list[dict[str, str | int | None]]) -> None:
        """Process a batch of file event dictionaries.

        Args:
            data_query (list[dict[str, str | int | None]]): A list of file event
                payloads that are forwarded to the handler.
        """
        for data in data_query:
            self.handler.process_data(data)


def main() -> None:
    """Start the IPC server and begin receiving messages."""
    ipc = IPC(
        ".\\..\\database\\data\\demo.db", ".\\..\\database\\data\\demo_archive.db"
    )
    ipc.receive()


if __name__ == "__main__":
    main()

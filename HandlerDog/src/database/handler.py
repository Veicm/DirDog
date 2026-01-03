import sqlite3
import json


class Handler:

    def __init__(self, db_path: str, archive_path: str) -> None:
        self.connection_db: sqlite3.Connection = sqlite3.connect(db_path)
        self.cursor_db: sqlite3.Cursor = self.connection_db.cursor()

        self.connection_archive: sqlite3.Connection = sqlite3.connect(archive_path)
        self.cursor_archive: sqlite3.Cursor = self.connection_archive.cursor()

        self.storage_path: str = ".\\data\\storage.json"  # TODO: Change path maybe

    def process_data(self, data: dict[str, str | int | None]) -> None:
        """
        This function takes the file data and decides, based on the
        provided information, which action should be executed.

        Args:
            data (dict[str, str | int | None]): The file data in the format, saved in api.json.

        Returns:
            None
        """
        match data.get("action"):
            case "Renamed":
                self.rename(data)

            case "Changed":
                self.change(data)

            case "Created":
                self.create(data)

            case "Deleted":
                self.delete(data)

            case _:
                raise ValueError(f"{data.get("action")} is not a valid action type.")

    def rename(self, data: dict[str, str | int | None]) -> None:
        """
        _ description _

        Args:
            data (dict[str, str | int | None]): The file data in the format, saved in api.json.

        Returns:
            None
        """
        raise NotImplementedError("function 'rename()' is not implemented yet.")

    def change(self, data: dict[str, str | int | None]) -> None:
        """
        This function is used to edit an entry by searching the file name and
        updating the meta data.

        Args:
            data (dict[str, str | int | None]): The file data in the format, saved in api.json.

        Returns:
            None
        """
        parent_dir: str | int | None = data.get("parent_dir")
        if not isinstance(parent_dir, str):
            raise ValueError(f"{parent_dir} is not a valid value of 'parent_dir'.")
        self.cursor_db.execute(f'SELECT * FROM "{parent_dir}"')
        entries: list[tuple[int, str, str, int, str]] = self.cursor_db.fetchall()
        for entry in entries:
            if entry[1] == data.get("file_name"):

                updated_entry: tuple[
                    int,
                    str | int | None,
                    str | int | None,
                    str | int | None,
                    str | int | None,
                ] = (
                    entry[0],
                    data.get("file_name"),
                    data.get("file_extension"),
                    data.get("last_modified"),
                    data.get("SHA-256-Hash"),
                )

                self.cursor_db.execute(
                    f'UPDATE "{parent_dir}" SET file_name = ?, file_extension = ?, last_modified = ?, hash = ? WHERE id = ?',
                    (
                        updated_entry[1],
                        updated_entry[2],
                        updated_entry[3],
                        updated_entry[4],
                        updated_entry[0],
                    ),
                )
        self.connection_db.commit()

    def create(self, data: dict[str, str | int | None]) -> None:
        """
        This function is used to create a new entry into the db.
        It creates a new table and adds the dir to 'known_dirs' in the storage.json file if needed.

        Args:
            data (dict[str, str | int | None]): The file data in the format, saved in api.json.

        Returns:
            None
        """
        parent_dir: str | int | None = data.get("parent_dir")
        if not isinstance(parent_dir, str):
            raise ValueError(f"{parent_dir} is not a valid value of 'parent_dir'.")
        if self._is_new_dir(parent_dir):
            self._add_new_dir_to_storage(parent_dir)
            self.cursor_db.execute(
                f'CREATE TABLE IF NOT EXISTS "{parent_dir}" (id INTEGER PRIMARY KEY, file_name TEXT NOT NULL, file_extension TEXT NOT NULL, last_modified INTEGER NOT NULL, hash TEXT NOT NULL)'
            )
        self.cursor_db.execute(
            f'INSERT INTO "{parent_dir}" VALUES (?, ?, ?, ?, ?)',
            (
                self._detect_gap(parent_dir, False),
                data.get("file_name"),
                data.get("file_extension"),
                data.get("last_modified"),
                data.get("SHA-256-Hash"),
            ),
        )
        self.connection_db.commit()

    def delete(self, data: dict[str, str | int | None]) -> None:
        """
        _ description _

        Args:
            data (dict[str, str | int | None]): The file data in the format, saved in api.json.

        Returns:
            None
        """
        raise NotImplementedError("function 'delete()' is not implemented yet.")

    ###############################################################################################################################

    def _is_new_dir(self, dir_path: str) -> bool:
        """
        This function checks if a give dir path is already known or not.

        Args:
            dir_path (str): The absolute path of the dir [Example: "C:\\path\\to\\dir"].

        Returns:
            bool: True if the dir is new and False if the dir is already known.
        """
        json_data = {}
        with open(self.storage_path) as json_file:
            json_data: dict[str, list[str]] = json.load(json_file)
        dir_list: list[str] | None = json_data.get("known_dirs")
        if dir_list is not None:
            for dir in dir_list:
                if dir_path == dir:
                    return False
        return True

    def _add_new_dir_to_storage(self, dir: str) -> None:
        """
        This function adds a new dir to the storage.json file.

        Args:
            dir (str): The dir, witch should be added to the storage.

        Returns:
            None
        """
        with open(self.storage_path) as json_file:
            json_data: dict[str, list[str]] = json.load(json_file)

        # Append new data
        if json_data.get("known_dirs") is not None:
            json_data["known_dirs"].append(dir)
        else:
            raise ValueError("known_dirs could not be found in storage.json.")

        # Write updated data back to the file
        with open(self.storage_path, "w") as json_file:
            json.dump(json_data, json_file, indent=4)

    def _detect_gap(self, table: str, archive: bool = False) -> int:
        """
        Find the first missing ID in the sequence of entries for a given table.
        This ensures that new entries are inserted at the correct position without
        leaving unused identifiers.

        Args:
            table (str): The name of the table which entry IDs should be examined.
            archive (bool): This argument is used to decide if the archive db
                should be used or not. Defaults to False.

        Returns:
            int: The next available ID. If no gaps exist, returns the next
                consecutive ID after the highest one.
        """
        if archive:
            self.cursor_archive.execute(f'SELECT * FROM "{table}"')
            entries: list[tuple[int, str, str, int, str]] = (
                self.cursor_archive.fetchall()
            )
        else:
            self.cursor_db.execute(f'SELECT * FROM "{table}"')
            entries: list[tuple[int, str, str, int, str]] = self.cursor_db.fetchall()

        is_null: bool = False
        last_id: int = 0
        for entry in entries:
            entry_id: int = entry[0]
            if entry_id == last_id + 1:
                if not is_null:
                    return 0
                last_id = entry_id
                continue
            elif entry_id == 0:
                is_null = True
                continue
            else:
                return last_id + 1

        # Ensures that a empty list starts with 0
        if entries == []:
            return 0

        return last_id + 1


def main() -> None:
    handler = Handler(".\\data\\demo.db", ".\\data\\demo_archive.db")

    handler.change(
        {
            "parent_dir": "C:\\path\\to\\dir_2",
            "file_name": "test_3.txt",
            "file_extension": ".txt",
            "new_path": None,
            "last_modified": 3767641720,
            "SHA-256-Hash": "5555862a78a4b7e6d382c58664b8e67c144b5cac754d78c29a811778dcd68199",
            "action": "Changed",
        }
    )


if __name__ == "__main__":
    main()

import sqlite3


class LogicHandler:
    """
    This class is used to handle the logic of the GUI.

    Attributes:
        data_storage_path (str): The path to the persistence storage.
    """

    def __init__(self, data_base_path: str) -> None:
        self.data_base_path: str = data_base_path

        self.connection_db: sqlite3.Connection = sqlite3.connect(self.data_base_path)
        self.cursor_db: sqlite3.Cursor = self.connection_db.cursor()

    def get_db_file_types(self) -> dict[str, int]:
        """
        Retrieve and count file extensions stored across all database tables
        that contain a ``file_extension`` column.

        This method inspects the SQLite schema, identifies all tables whose
        CREATE statement references a ``file_extension`` column, extracts all
        non-null file extensions from those tables, and returns a dictionary
        mapping each extension to its occurrence count.

        Returns:
            dict[str, int]: A dictionary where keys are file extensions and
            values are the number of times each extension appears.

        Raises:
            RuntimeError: If no tables containing a ``file_extension`` column
            are found in the database.
        """
        self.cursor_db.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND sql LIKE '%file_extension%'
            """
        )

        tables = [row[0] for row in self.cursor_db.fetchall()]

        if not tables:
            raise RuntimeError("No tables with column 'file_extension' found.")

        union_sql = " UNION ALL ".join(
            f"SELECT file_extension FROM {table}" for table in tables
        )

        self.cursor_db.execute(union_sql)
        rows = self.cursor_db.fetchall()

        file_extensions: list[str] = [row[0] for row in rows if row[0] is not None]

        return self._sort_and_count_file_types(file_extensions)

    def _sort_and_count_file_types(self, file_extensions: list[str]) -> dict[str, int]:
        """
        Count occurrences of file extensions in a list.

        This method iterates over the given list of file extensions and builds
        a dictionary containing the frequency of each unique extension.

        Args:
            file_extensions (list[str]): A list of file extension strings.

        Returns:
            dict[str, int]: A dictionary mapping each file extension to the
            number of times it occurs in the input list.
        """
        result: dict[str, int] = {}
        know_extentions: list[str] = []

        for extension in file_extensions:
            if extension in know_extentions:
                result[extension] += 1
            else:
                know_extentions.append(extension)
                result[extension] = 1

        return result

class LogicHandler:
    """
    This class is used to handel the logic of the GUI.

    Attributes:
        data_storage_path (str): The path to the persistence storage.
    """

    def __init__(self, data_storage_path: str) -> None:
        self.data_storage_path: str = data_storage_path

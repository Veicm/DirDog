from database.handler import Handler


class IPS:
    def __init__(self) -> None:
        self.handler = Handler()

    def dummy_receiver() -> None:
        """
        _ description _

        Args:
            variable (any): _ variable description _.

        Returns:
            int: _ value description _.
        """
        self.handler.process_data(file_data)

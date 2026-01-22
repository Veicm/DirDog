import random
from PySide6.QtCore import QTimer, QObject, Signal
from backend.backroud_logic import LogicHandler

class DataController(QObject):
    pie_data_updated = Signal(dict)

    def __init__(self):
        super().__init__()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)
        self.logic_handler = LogicHandler(r"../../HandlerDog/src/database/data/demo.db")

    # === DATA SOURCE INTERFACE ===
    # Replace this method later with real application data
    def update_data(self):
        data = self.logic_handler.get_db_file_types()
        self.pie_data_updated.emit(data)

    # === EXTERNAL DATA INTERFACE ===
    # You can call this manually to push data from outside
    def set_pie_data(self, data: dict[str, float]):
        self.pie_data_updated.emit(data)

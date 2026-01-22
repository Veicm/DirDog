from frontend.data_controller.controller import DataController
from .dashboard import DashboardPage

from PySide6.QtWidgets import QMainWindow



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Admin Dashboard")
        self.resize(800, 500)

        self.controller = DataController()

        self.dashboard = DashboardPage(self.controller)
        self.setCentralWidget(self.dashboard)

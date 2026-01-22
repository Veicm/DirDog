from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt
from frontend.data_controller.controller import DataController
from .widgets.header import HeaderWidget
from .widgets.footer import FooterWidget
from .widgets.pi_chart import PieChartWidget
from .widgets.PathListWidget import PathListWidget  # readonly Pfadfeld


class DashboardPage(QWidget):
    def __init__(self, controller: DataController):
        super().__init__()

        # --- Main layout ---
        main_layout = QVBoxLayout(self)

        # --- Header ---
        self.header_widget = HeaderWidget()
        main_layout.addWidget(self.header_widget)

        # --- Content layout (PieChart + Status fields) ---
        content_layout = QHBoxLayout()

        # --- PieChart (LEFT) ---
        self.pie_chart = PieChartWidget("File Types")
        content_layout.addWidget(self.pie_chart, 2)  # stretch factor 2

        # --- Right status fields ---
        status_layout = QVBoxLayout()

        # Process 1
        self.process1_status = QLabel("Process 1: Idle")
        self.process1_status.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.process1_status.setStyleSheet("background-color: #222; color: white; padding: 5px;")
        self.process1_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.process1_status.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        status_layout.addWidget(self.process1_status, 1)  # stretch factor 1

        # Process 2
        self.process2_status = QLabel("Process 2: Idle")
        self.process2_status.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.process2_status.setStyleSheet("background-color: #222; color: white; padding: 5px;")
        self.process2_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.process2_status.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        status_layout.addWidget(self.process2_status, 1)  # stretch factor 1

        # Extra stretch to push widgets to top if content grows
        status_layout.addStretch(1)

        # --- Add the status layout to the content layout ---
        content_layout.addLayout(status_layout, 1)  # stretch factor 1 for right panel

        # --- Add content to main layout ---
        main_layout.addLayout(content_layout, 1)  # content takes remaining space

        # --- Path input (BOTTOM) ---
        self.path_widget = PathListWidget()
        main_layout.addWidget(self.path_widget)

        # --- Controller connection ---
        controller.pie_data_updated.connect(self.pie_chart.update_data)
        
    # =====================
    # === DATA INTERFACES ===
    # =====================

    # --- PieChart interface ---
    def set_pie_data(self, data: dict[str, float]):
        """Update pie chart with new data"""
        self.pie_chart.update_data(data)




    # --- Process status interfaces ---
    def set_process1_status(self, text: str):
        """Update Process 1 status"""
        self.process1_status.setText(text)

    def set_process2_status(self, text: str):
        """Update Process 2 status"""
        self.process2_status.setText(text)

    # --- PathList interface ---
    def add_path(self, path: str):
        """Add a new path to the PathList widget"""
        self.path_widget.add_path_to_GUI(path)

    def get_paths(self) -> list[str]:
        """Get all paths from PathList widget"""
        return self.path_widget.get_paths()

    def clear_paths(self):
        """Clear all paths from PathList widget"""
        self.path_widget.clear_paths()

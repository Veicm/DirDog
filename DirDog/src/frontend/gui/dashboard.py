from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QSizePolicy,QPushButton
)
import time
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer,QProcess
import os
from frontend.data_controller.controller import DataController
from .widgets.header import HeaderWidget
from .widgets.footer import FooterWidget
from .widgets.pi_chart import PieChartWidget
from .widgets.PathListWidget import PathListWidget  # readonly Pfadfeld


class DashboardPage(QWidget):
    def __init__(self, controller: DataController):
        super().__init__()
        self.process1 = QProcess(self)
        self.process2 = QProcess(self)

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
        # --- Process 1 ---
        p1_layout = QHBoxLayout()

        self.process1_status = QLabel("Process 1: Idle")
        self.process1_status.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.process1_status.setAlignment(Qt.AlignCenter)

        self.process1_button = QPushButton("Start")
        self.process1_button.clicked.connect(
            lambda: self.start_process(
                os.path.join(
                    str(os.environ.get("ProgramFiles")),
                    "DirDog",
                    "HandlerDog_exe",
                    "HandlerDog.exe",
                )
            )
        )


        p1_layout.addWidget(self.process1_status, 3)
        p1_layout.addWidget(self.process1_button, 1)

        status_layout.addLayout(p1_layout)




        # Process 2
        p2_layout = QHBoxLayout()

        self.process2_status = QLabel("Process 1: Idle")
        self.process2_status.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.process2_status.setAlignment(Qt.AlignCenter)

        self.process2_button = QPushButton("Start")
        self.process2_button.clicked.connect(
            lambda: self.start_process(
                os.path.join(
                    str(os.environ.get("ProgramFiles")),
                    "DirDog",
                    "SentinelDog_exe",
                    "SentinelDog.exe",
                )
            )
        )


        p2_layout.addWidget(self.process2_status, 3)
        p2_layout.addWidget(self.process2_button, 1)

        status_layout.addLayout(p1_layout)

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
        self._init_status_timer()
        
    # =====================
    # === DATA INTERFACES ===
    # =====================
    def update_status(self):
        status=DataController.get_status_of_processes()
        self.process1_status.setText(f"Process: {status[0]}")
        self.process2_status.setText(f"Process: {status[1]}")

    def _init_status_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)  # alle 1000 ms


    def start_process(self,Path):
        self.process2.start(Path)





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

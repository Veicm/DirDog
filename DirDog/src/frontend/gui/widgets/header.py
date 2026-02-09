import sys
import random

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QCheckBox
)
from PySide6.QtCore import QTimer
import pyqtgraph as pg
import os
import json
class HeaderWidget(QWidget):
    def __init__(self):

        super().__init__()
        self.config_path = str(os.getenv("APPDATA")) + r"\DirDog\config\data_storage.json"
        with open(self.config_path, "r") as f:
            config = json.load(f)
        self.toggle_value = config["auto_start"]


        layout = QHBoxLayout(self)

        title = QLabel("DirDog – Dashboard")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")


        label = QLabel("Autostart")

        self.toggle = QCheckBox()
        self.toggle.setChecked(self.toggle_value)
        self.toggle.stateChanged.connect(self._on_toggle_changed)

        

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.toggle)
        layout.addWidget(label)


    def _on_toggle_changed(self, state: int):
        self.toggle_value = bool(state)



        with open(self.config_path, "r") as f:
            config = json.load(f)

        config["auto_start"] = self.toggle_value

        with open(self.config_path,"w") as file:
            json.dump(config,file,indent=4)
        
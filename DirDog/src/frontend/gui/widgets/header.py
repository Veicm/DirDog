import sys
import random

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel
)
from PySide6.QtCore import QTimer
import pyqtgraph as pg

class HeaderWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        title = QLabel("DirDog – Dashboard")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        status = QLabel("Status: OK")

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(status)

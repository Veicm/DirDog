from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel


class FooterWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        info = QLabel("Bereit")
        version = QLabel("v0.1")

        layout.addWidget(info)
        layout.addStretch()
        layout.addWidget(version)

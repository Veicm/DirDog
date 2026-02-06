from PySide6.QtWidgets import QApplication
import sys
from frontend.gui.window import MainWindow
import os

if __name__ == "__main__":
    path: str = os.path.join(os.getenv("APPDATA"), "DirDog")
    os.chmod(path, 0o666)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

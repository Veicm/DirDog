from PySide6.QtWidgets import QApplication
import sys
from frontend.gui.window import MainWindow
import os

if __name__ == "__main__":
    os.chmod(os.getenv("APPDATA") + r"\DirDog",0o666 )
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

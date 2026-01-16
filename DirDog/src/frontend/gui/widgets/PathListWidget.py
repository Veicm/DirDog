from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QFileDialog
)

class PathListWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # --- Input Row ---
        input_layout = QHBoxLayout()

        self.browse_btn = QPushButton("Browse...")


        input_layout.addWidget(self.browse_btn)


        layout.addLayout(input_layout)

        # --- Path List ---
        self.path_list = QListWidget()
        self.path_list.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.path_list, 1)  # stretch = scrollable

        # --- Remove Button ---
        self.remove_btn = QPushButton("Remove Selected")
        layout.addWidget(self.remove_btn)

        # --- Signals ---
        self.browse_btn.clicked.connect(self.browse_path)
        self.remove_btn.clicked.connect(self.remove_selected)

    # === DATA INTERFACE ===
    def add_path(self, path: str = None):
        """Add a new path, either from parameter or input field"""
        if path is None:
            path = self.path_input.text()
        if path:
            self.path_list.addItem(path)
            self.path_input.clear()

    def remove_selected(self):
        """Remove selected paths"""
        for item in self.path_list.selectedItems():
            self.path_list.takeItem(self.path_list.row(item))

    def browse_path(self):
        """Open a file/folder dialog and add the selected path"""
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if path:
            self.add_path(path)

    # === DATA INTERFACE ===
    def get_paths(self) -> list[str]:
        """Return all paths currently in the list"""
        return [self.path_list.item(i).text() for i in range(self.path_list.count())]

    def clear_paths(self):
        """Clear all paths"""
        self.path_list.clear()

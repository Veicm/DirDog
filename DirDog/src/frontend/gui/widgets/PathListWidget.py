from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QFileDialog
)
import json
from pathlib import Path
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

        self.config_path = Path(
                ".\\data\\data_storage.json"
            )

        self.load_paths_into_GUI()




    def add_selected_to_json(self,input: str) -> None:
        with open(".\\data\\data_storage.json","r") as file:
            data: dict[str,bool | list[str]] = json.load(file)
        

        data["monitoring_dirs"].append(input)

        with open(".\\data\\data_storage.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, sort_keys=True, ensure_ascii=False)
        

    def load_paths_into_GUI(self):

        with self.config_path.open("r",encoding="utf-8") as file:
            data = json.load(file)
        
        for path in data["monitoring_dirs"]:
            if path is None:
                path = self.path_input.text()
            if path:
                self.path_list.addItem(path)
        

    # === DATA INTERFACE ===
    def add_path_to_GUI(self, path: str = None):
        """Add a new path, either from parameter or input field"""
        if path is None:
            path = self.path_input.text()
        if path:
            self.path_list.addItem(path)
            self.add_selected_to_json(str(Path(path).resolve()))

    def remove_selected(self):
        """Remove selected paths"""
        with self.config_path.open("r",encoding="utf-8") as file:
            data = json.load(file)

        
        for item in self.path_list.selectedItems():
            path = item.text()
            
            
            self.path_list.takeItem(self.path_list.row(item))
            

            data["monitoring_dirs"] = [
                p for p in data["monitoring_dirs"]
                if str(Path(p).resolve()) != str(Path(path).resolve())
            ]
            
        with self.config_path.open("w",encoding="utf-8") as file:
            json.dump(data,file, indent=2,ensure_ascii=False)




    def browse_path(self):
        """Open a file/folder dialog and add the selected path"""
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if path:
            self.add_path_to_GUI(path)

    # === DATA INTERFACE ===
    def get_paths(self) -> list[str]:
        """Return all paths currently in the list"""
        return [self.path_list.item(i).text() for i in range(self.path_list.count())]

    def clear_paths(self):
        """Clear all paths"""
        self.path_list.clear()

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                            QLineEdit, QPushButton, QLabel, QComboBox)
from PyQt6.QtCore import Qt

class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Search NBT")
        layout = QVBoxLayout(self)
        
        # Search type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Search in:"))
        self.search_type = QComboBox()
        self.search_type.addItems(["Tag Names", "Tag Values", "Both"])
        type_layout.addWidget(self.search_type)
        layout.addLayout(type_layout)
        
        # Search text
        text_layout = QHBoxLayout()
        text_layout.addWidget(QLabel("Search for:"))
        self.search_text = QLineEdit()
        text_layout.addWidget(self.search_text)
        layout.addLayout(text_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.search_button = QPushButton("Search")
        self.cancel_button = QPushButton("Cancel")
        self.search_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout) 
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                            QTextEdit, QLabel, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor

class HexHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.byte_format = QTextCharFormat()
        self.byte_format.setBackground(QColor("#3d3d3d"))
        self.ascii_format = QTextCharFormat()
        self.ascii_format.setBackground(QColor("#353535"))

    def highlightBlock(self, text):
        # Highlight hex values
        for i in range(0, len(text), 3):
            if i + 2 < len(text):
                self.setFormat(i, 2, self.byte_format)
        # Highlight ASCII representation
        ascii_start = text.find("|") + 1
        if ascii_start > 0:
            self.setFormat(ascii_start, len(text) - ascii_start, self.ascii_format)

class HexViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Hex Viewer")
        header.setStyleSheet("""
            font-weight: bold; 
            font-size: 14px; 
            padding: 5px;
            color: #ffffff;
        """)
        layout.addWidget(header)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
            }
        """)
        layout.addWidget(scroll)
        
        # Create container widget
        container = QWidget()
        scroll.setWidget(container)
        container_layout = QVBoxLayout(container)
        
        # Create hex display
        self.hex_display = QTextEdit()
        self.hex_display.setReadOnly(True)
        self.hex_display.setFont(QFont("Consolas", 10))
        self.hex_display.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                padding: 5px;
            }
        """)
        
        # Add syntax highlighter
        self.highlighter = HexHighlighter(self.hex_display.document())
        
        container_layout.addWidget(self.hex_display)
        
        # Add status bar
        self.status_label = QLabel()
        self.status_label.setStyleSheet("""
            padding: 5px; 
            color: #aaaaaa;
            background-color: #2d2d2d;
        """)
        layout.addWidget(self.status_label)
        
    def display_data(self, data):
        if not data:
            self.hex_display.clear()
            self.status_label.setText("No binary data to display")
            return
            
        hex_lines = []
        total_bytes = len(data)
        
        for i in range(0, len(data), 16):
            chunk = data[i:i+16]
            # Format hex values
            hex_values = ' '.join(f'{b:02x}' for b in chunk)
            # Format ASCII representation
            ascii_values = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
            # Add padding for alignment
            hex_values = hex_values.ljust(47)
            # Combine into a line
            hex_lines.append(f'{i:08x}: {hex_values} | {ascii_values}')
            
        self.hex_display.setText('\n'.join(hex_lines))
        self.status_label.setText(f"Total bytes: {total_bytes}") 
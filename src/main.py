import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from nbtlib.tag import (Compound, List, String, Int, Byte, 
                       Short, Long, Float, Double, ByteArray, 
                       IntArray, LongArray)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 
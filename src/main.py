"""Main of WADAS application."""

import sys
from PySide6.QtWidgets import QApplication
from domain.mainwindow import MainWindow

def main():
    """Main function to lunch mainwindow."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

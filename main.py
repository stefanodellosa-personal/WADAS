"""Main of WADAS application."""

import platform
import sys

from PySide6.QtWidgets import QApplication

from wadas.ui.mainwindow import MainWindow


def main():
    """Main function to lunch mainwindow."""

    app = QApplication(sys.argv)
    system = platform.system()
    if system == "Windows":
        # Force style to avoid Win 11 issue with disabled icons not grayed out.
        app.setStyle("fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

"""Module containing logic to draw license dialog."""

import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QTextEdit
from PySide6.QtGui import QIcon

module_dir_path = os.path.dirname(os.path.abspath(__file__))


class LicenseDialog(QDialog):
    """Class to represent LICENSE file in a QDialog"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("License")
        self.setGeometry(150, 150, 450, 400)
        self.setWindowIcon(QIcon(os.path.join(module_dir_path, "..", "img", "mainwindow_icon.jpg")))

        layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        layout.addWidget(self.text_edit)

        # Load license file
        license_dir = os.path.abspath(os.path.join(module_dir_path, "..", ".."))
        license_path = os.path.join(license_dir, "LICENSE")
        with open(license_path, 'r') as file:
            license_text = file.read()
            self.text_edit.setPlainText(license_text)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)
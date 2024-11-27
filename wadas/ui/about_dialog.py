"""Module containing logic to show About WADAS info in dedicated dialog."""

import os

from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton
from PySide6.QtGui import QIcon

from wadas._version import __version__

module_dir_path = os.path.dirname(os.path.abspath(__file__))


class AboutDialog(QDialog):
    """Class to show About WADAS info in dedicated dialog."""
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set dialog properties
        self.setWindowTitle("About WADAS")
        self.setGeometry(150, 150, 500, 300)
        self.setWindowIcon(QIcon(os.path.join(module_dir_path, "..", "img", "mainwindow_icon.jpg")))

        # Create layout
        layout = QVBoxLayout()

        # Add read-only QTextEdit for the about text
        about_text = QTextBrowser(self)
        about_text.setReadOnly(True)  # Make it read-only
        about_text.setText(
            f"""<h2>Wild Animal Detection and Alert System</h2>
            <p>Wild Animal Detection and Alert System (WADAS) is a project for
            AI-based detection and classification wildlife, capable of producing
            notification and actuate remote devices to prevent fatal accidents involving
            wild animals or act as prevention measure to improve animal-to-humans
            coexistence.</p>
            <p>WADAS goal is to protect wildlife. Any misuse causing harm or even death
            of animals is discouraged and forbidden.</p>
            <p>Version: {__version__}</p>
            <p>Developed by: Stefano Dell'Osa,
             Alessandro Palla,
             Antonio Farina,
             Cesare Di Mauro.</p>
            <p>For more information, visit our <a href='https://github.com/stefanodellosa-personal/WADAS'>GitHub</a>.</p>
            """
        )
        about_text.setOpenExternalLinks(True)  # Allow opening links in a browser
        layout.addWidget(about_text)

        # Add a close button
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        # Set the layout
        self.setLayout(layout)

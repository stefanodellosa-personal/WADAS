"""Insert URL module."""

import os

import validators
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QDialogButtonBox

from wadas.ui.ui_insert_url import Ui_InsertUrlDialog


class InsertUrlDialog(QDialog, Ui_InsertUrlDialog):
    """Class to allow URL insertion from dialog."""

    def __init__(self):
        super(InsertUrlDialog, self).__init__()
        self.ui = Ui_InsertUrlDialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), "img", "mainwindow_icon.jpg")))
        self.url = ""
        self.ui.buttonBox.accepted.connect(self.accept_and_close)
        self.ui.lineEdit_url.textChanged.connect(self.validate_url)
        # TODO: uncomment line below if no URL is provided by default
        # self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def accept_and_close(self):
        """When Ok is clicked, save url before closing."""
        self.url = self.ui.lineEdit_url.text()
        self.accept()

    def validate_url(self):
        """Check if inserted URL is valid."""

        url = self.ui.lineEdit_url.text()
        is_validated = bool(validators.url(url))
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(is_validated)

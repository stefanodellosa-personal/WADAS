from ui.ui_insert_url import Ui_InsertUrlDialog
from PySide6.QtWidgets import QDialog, QDialogButtonBox
from ui.error_dialog import ErrorMessage
import validators

class InsertUrlDialog(QDialog, Ui_InsertUrlDialog):
    def __init__(self):
        super(InsertUrlDialog, self).__init__()
        self.ui = Ui_InsertUrlDialog()
        self.ui.setupUi(self)
        self.url = ""
        self.ui.buttonBox.accepted.connect(self.accept_and_close)
        self.ui.lineEdit_url.textChanged.connect(self.validate_url)
        # TODO: uncomment line below if no URL is provided by default
        #self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def accept_and_close(self):
        """When Ok is clicked, save url before closing."""
        self.url = self.ui.lineEdit_url.text()
        self.accept()

    
    def validate_url(self):
        """Check if inserted URL is valid."""

        url = self.ui.lineEdit_url.text()
        if validators.url(url):
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

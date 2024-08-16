from ui.ui_insert_url import Ui_InsertUrlDialog
from PySide6.QtWidgets import QDialog

class InsertUrlDialog(QDialog, Ui_InsertUrlDialog):
    def __init__(self):
        super(InsertUrlDialog, self).__init__()
        self.ui = Ui_InsertUrlDialog()
        self.ui.setupUi(self)
        self.url = ""
        self.ui.buttonBox.accepted.connect(self.accept_and_close)

    def accept_and_close(self):
        """When Ok is clicked, save url before closing."""

        #TODO: add invalid URL handling
        self.url = self.ui.lineEdit_url.text()
        self.accept()
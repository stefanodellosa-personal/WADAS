import validators
from PySide6.QtWidgets import QDialog, QDialogButtonBox
from ui.ui_insert_email import Ui_DialogInsertEmail

class DialogInsertEmail(QDialog, Ui_DialogInsertEmail):
    def __init__(self):
        super(DialogInsertEmail, self).__init__()
        self.ui = Ui_DialogInsertEmail()
        self.ui.setupUi(self)
        self.sender_email = ""
        self.smtp_server = ""
        self.smtp_port = ""
        self.password = ""
        self.valid_email = False
        self.valid_smtp = False
        self.valid_port = False
        self.valid_password = False
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.pushButton_testEmail.setEnabled(False)

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)
        self.ui.lineEdit_senderEmail.textChanged.connect(self.validate_email)
        self.ui.lineEdit_smtpServer.textChanged.connect(self.validate_smtp_server)
        self.ui.lineEdit_port.textChanged.connect(self.validate_smtp_port)
        self.ui.lineEdit_password.textChanged.connect(self.validate_password)

    def accept_and_close(self):
        """When Ok is clicked, save email config info before closing."""
        self.sender_email = self.ui.lineEdit_senderEmail.text()
        self.smtp_server = self.ui.lineEdit_smtpServer.text()
        self.smtp_port = self.ui.lineEdit_port.text()
        self.password = self.ui.lineEdit_password.text()
        self.accept()

    def validate_email_configurations(self):
        """Check if inserted email config is valid."""

        if self.valid_email and self.valid_smtp and self.valid_port and self.valid_password:
            self.ui.label_status.setText("")
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
   
    def validate_smtp_port(self):
        if self.ui.lineEdit_port.text().isdigit() and 1 <= int(self.ui.lineEdit_port.text()) <= 65535:
            self.valid_port = True
            self.validate_email_configurations()
        else:
            self.valid_port = False
            self.ui.label_status.setText("Invalid smtp port provided!")

    def validate_email(self):
        if validators.email(self.ui.lineEdit_senderEmail.text()):
            self.valid_email = True
            self.validate_email_configurations()
        else:
            self.valid_email = False
            self.ui.label_status.setText("Invalid sender email provided!")
    
    def validate_smtp_server(self):
        if self.ui.lineEdit_smtpServer.text():
            self.valid_smtp = True
            self.validate_email_configurations()
        else:
            self.valid_smtp = False
            self.ui.label_status.setText("Invalid smtp server provided!")
    
    def validate_password(self):
        if self.ui.lineEdit_password.text():
            self.valid_password = True
            self.validate_email_configurations()
        else:
            self.valid_password = False
            self.ui.label_status.setText("Invalid password provided!")

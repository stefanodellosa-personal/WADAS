"""Email configuration module."""

from PySide6.QtWidgets import QDialog, QDialogButtonBox
import keyring
import validators

from ui.ui_insert_email import Ui_DialogInsertEmail

class DialogInsertEmail(QDialog, Ui_DialogInsertEmail):
    """Class to insert email configuration to enable WADAS for email notifications."""
    def __init__(self, email_configuration):
        super(DialogInsertEmail, self).__init__()
        self.ui = Ui_DialogInsertEmail()
        self.ui.setupUi(self)
        self.email_configuration = email_configuration

        self.valid_sender_email = False
        self.valid_smtp = False
        self.valid_port = False
        self.valid_password = False
        self.valid_receiver_emails = False
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.pushButton_testEmail.setEnabled(False)

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)
        self.ui.lineEdit_senderEmail.textChanged.connect(self.validate_sender_email)
        self.ui.lineEdit_smtpServer.textChanged.connect(self.validate_smtp_server)
        self.ui.lineEdit_port.textChanged.connect(self.validate_smtp_port)
        self.ui.lineEdit_password.textChanged.connect(self.validate_password)
        self.ui.lineEdit_rec_email1.textChanged.connect(self.validate_receivers_email)
        self.ui.lineEdit_rec_email2.textChanged.connect(self.validate_receivers_email)
        self.ui.lineEdit_rec_email3.textChanged.connect(self.validate_receivers_email)
        self.ui.lineEdit_rec_email4.textChanged.connect(self.validate_receivers_email)
        self.ui.lineEdit_rec_email5.textChanged.connect(self.validate_receivers_email)
        self.ui.lineEdit_rec_email6.textChanged.connect(self.validate_receivers_email)
        self.ui.lineEdit_rec_email7.textChanged.connect(self.validate_receivers_email)
        self.ui.lineEdit_rec_email8.textChanged.connect(self.validate_receivers_email)
        self.ui.lineEdit_rec_email9.textChanged.connect(self.validate_receivers_email)
        self.ui.lineEdit_rec_email10.textChanged.connect(self.validate_receivers_email)

        self.initialize_form()

    def initialize_form(self):
        """Method to initialize form with existing email configuration data (if any)."""

        self.ui.lineEdit_smtpServer.setText(self.email_configuration['smtp_hostname'])
        self.ui.lineEdit_port.setText(self.email_configuration['smtp_port'])
        credentials = keyring.get_credential("WADAS_email", "")
        self.ui.lineEdit_senderEmail.setText(credentials.username)
        self.ui.lineEdit_password.setText(credentials.password)
        self.validate_email_configurations()

    def accept_and_close(self):
        """When Ok is clicked, save email config info before closing."""
        self.email_configuration['smtp_server'] = self.ui.lineEdit_smtpServer.text()
        self.email_configuration['smtp_port'] = self.ui.lineEdit_port.text()
        keyring.set_password("WADAS_email", self.ui.lineEdit_senderEmail.text(),
                              self.ui.lineEdit_password.text())
        self.accept()

    def validate_email_configurations(self):
        """Check if inserted email config is valid."""

        if self.valid_sender_email and self.valid_smtp and self.valid_port and self.valid_password and self.valid_receiver_emails:
            self.ui.label_status.setText("")
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def validate_smtp_port(self):
        """Method to validate smtp port."""

        if (text := self.ui.lineEdit_port.text()).isdigit() and 1 <= int(text) <= 65535:
            self.valid_port = True
            self.validate_email_configurations()
        else:
            self.valid_port = False
            self.ui.label_status.setText("Invalid smtp port provided!")

    def validate_sender_email(self):
        """Method to validate email format."""

        if validators.email(self.ui.lineEdit_senderEmail.text()):
            self.valid_sender_email = True
            self.validate_email_configurations()
        else:
            self.valid_sender_email = False
            self.ui.label_status.setText("Invalid sender email provided!")

    def validate_smtp_server(self):
        """Method to validate smtp hostname."""

        if self.ui.lineEdit_smtpServer.text():
            self.valid_smtp = True
            self.validate_email_configurations()
        else:
            self.valid_smtp = False
            self.ui.label_status.setText("Invalid smtp server provided!")

    def validate_password(self):
        """Method to validate password."""

        if self.ui.lineEdit_password.text():
            self.valid_password = True
            self.validate_email_configurations()
        else:
            self.valid_password = False
            self.ui.label_status.setText("Invalid password provided!")

    def validate_receivers_email(self):
        """Method to validate receiver email(s)."""

        if (email1 := self.ui.lineEdit_rec_email1.text()) and validators.email(email1):
            self.valid_receiver_emails = True
            self.validate_email_configurations()
        else:
            self.valid_receiver_emails = False
            self.ui.label_status.setText("Invalid receiver email1 provided!")

        email2 = self.ui.lineEdit_rec_email2.text()
        if email2:
            if validators.email(email2):
                self.valid_receiver_emails = True
                self.validate_email_configurations()
            else:
                self.valid_receiver_emails = False
                self.ui.label_status.setText("Invalid receiver email2 provided!")

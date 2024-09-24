"""Email configuration module."""


import os
import keyring
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import smtplib

import validators
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QDialogButtonBox

from src.ui.ui_insert_email import Ui_DialogInsertEmail

class DialogInsertEmail(QDialog, Ui_DialogInsertEmail):
    """Class to insert email configuration to enable WADAS for email notifications."""

    def __init__(self, email_configuration):
        super(DialogInsertEmail, self).__init__()
        self.ui = Ui_DialogInsertEmail()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(
            os.getcwd(), "src", "img","mainwindow_icon.jpg")))

        self.email_configuration = email_configuration
        self.valid_sender_email = False
        self.valid_smtp = False
        self.valid_port = False
        self.valid_password = False
        self.valid_receiver_emails = False
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.pushButton_testEmail.setEnabled(False)
        self.ui.label_status.setStyleSheet("color: red")

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)
        self.ui.lineEdit_senderEmail.textChanged.connect(self.validate_sender_email)
        self.ui.lineEdit_smtpServer.textChanged.connect(self.validate_smtp_server)
        self.ui.lineEdit_port.textChanged.connect(self.validate_smtp_port)
        self.ui.lineEdit_password.textChanged.connect(self.validate_password)
        self.ui.textEdit_recipient_email.textChanged.connect(self.validate_recipients_email)
        self.ui.pushButton_testEmail.clicked.connect(self.send_email)

        self.initialize_form()

    def initialize_form(self):
        """Method to initialize form with existing email configuration data (if any)."""

        self.ui.lineEdit_smtpServer.setText(self.email_configuration['smtp_hostname'])
        self.ui.lineEdit_port.setText(self.email_configuration['smtp_port'])
        credentials = keyring.get_credential("WADAS_email", "")
        self.ui.lineEdit_senderEmail.setText(credentials.username)
        self.ui.lineEdit_password.setText(credentials.password)
        if recipients_email := self.email_configuration['recipients_email']:
            recipients = ', '.join(recipients_email)
            self.ui.textEdit_recipient_email.setText(recipients)
        self.validate_email_configurations()

    def accept_and_close(self):
        """When Ok is clicked, save email config info before closing."""
        self.email_configuration['smtp_hostname'] = self.ui.lineEdit_smtpServer.text()
        self.email_configuration['smtp_port'] = self.ui.lineEdit_port.text()
        self.email_configuration['recipients_email'] = list()
        for recipient in self.ui.textEdit_recipient_email.toPlainText().strip().split(", "):
            self.email_configuration['recipients_email'].append(recipient)
        keyring.set_password("WADAS_email", self.ui.lineEdit_senderEmail.text(),
                              self.ui.lineEdit_password.text())
        self.accept()

    def validate_email_configurations(self):
        """Check if inserted email config is valid."""

        if (self.valid_sender_email and self.valid_smtp and self.valid_port and
            self.valid_password and self.valid_receiver_emails):
            self.ui.label_status.setText("")
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            self.ui.pushButton_testEmail.setEnabled(True)
        else:
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            self.ui.pushButton_testEmail.setEnabled(False)

    def validate_smtp_port(self):
        """Method to validate smtp port."""

        if (text := self.ui.lineEdit_port.text()).isdigit() and 1 <= int(text) <= 65535:
            self.valid_port = True
        else:
            self.valid_port = False
            self.ui.label_status.setText("Invalid smtp port provided!")
        self.validate_email_configurations()

    def validate_sender_email(self):
        """Method to validate email format."""

        if validators.email(self.ui.lineEdit_senderEmail.text()):
            self.valid_sender_email = True
        else:
            self.valid_sender_email = False
            self.ui.label_status.setText("Invalid sender email provided!")
        self.validate_email_configurations()

    def validate_smtp_server(self):
        """Method to validate smtp hostname."""

        if self.ui.lineEdit_smtpServer.text():
            self.valid_smtp = True
        else:
            self.valid_smtp = False
            self.ui.label_status.setText("Invalid smtp server provided!")
        self.validate_email_configurations()

    def validate_password(self):
        """Method to validate password."""

        if self.ui.lineEdit_password.text():
            self.valid_password = True
        else:
            self.valid_password = False
            self.ui.label_status.setText("Invalid password provided!")
        self.validate_email_configurations()

    def validate_recipients_email(self):
        """Method to validate receiver email(s)."""

        recipients_email = self.ui.textEdit_recipient_email.toPlainText().strip()
        if recipients_email:
            emails = recipients_email.split(", ")
            for email in emails:
                if not validators.email(email):
                    self.valid_receiver_emails = False
                    self.ui.label_status.setText("Invalid recipients email(s) provided!")
                else:
                    self.valid_receiver_emails = True
        else:
            self.valid_receiver_emails = False
            self.ui.label_status.setText("No recipients email provided!")
        self.validate_email_configurations()

    def send_email(self):
        """Method to test email."""

        credentials = keyring.get_credential("WADAS_email", "")
        sender = credentials.username
        recipients = [recipient for recipient in self.ui.textEdit_recipient_email.toPlainText().strip().split(", ")]

        text = "WADAS test email."
        message = MIMEText(text, "plain")

        message['Subject'] = "WADAS test email"
        message['From'] = sender
        message['To'] = self.ui.textEdit_recipient_email.toPlainText().strip()

        # Connect to Gmail's SMTP server using SSL.
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.ui.lineEdit_smtpServer.text(),
                               self.ui.lineEdit_port.text(),
                               context=context) as smtp_server:

            smtp_server.login(sender, credentials.password)

            for recipient in recipients:
                smtp_server.sendmail(sender, recipient, message.as_string())
        self.ui.label_status.setText("Test email(s) sent!")

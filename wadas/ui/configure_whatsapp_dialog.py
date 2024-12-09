"""Whatsapp configuration module."""


import os

import keyring
import validators
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QDialogButtonBox

from wadas.domain.notifier import Notifier
from wadas.ui.qt.ui_configure_whatsapp import Ui_DialogConfigureWhatsApp

module_dir_path = os.path.dirname(os.path.abspath(__file__))


class DialogConfigureWhatsApp(QDialog, Ui_DialogConfigureWhatsApp):
    """Class to insert WhatsApp configuration data to enable WADAS for WhatsApp notifications."""

    def __init__(self):
        super(DialogConfigureWhatsApp, self).__init__()
        self.ui = Ui_DialogConfigureWhatsApp()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(module_dir_path, "..", "img", "mainwindow_icon.jpg")))
        self.ui.pushButton_testMessage.setEnabled(False)
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.label_errorMessage.setStyleSheet("color: red")

        self.whatsapp_notifier = Notifier.notifiers[Notifier.NotifierTypes.WHATSAPP.value]

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)

        self.initialize_form()

    def initialize_form(self):
        """Method to initialize form with existing email configuration data (if any)."""

        if Notifier.notifiers[Notifier.NotifierTypes.EMAIL.value]:
            self.ui.checkBox_enableWhatsAppNotifications.setEnabled(self.whatsapp_notifier.enabled)
            self.ui.lineEdit_phoneID.setText(self.whatsapp_notifier.sender_id)
        else:
            self.ui.checkBox_enableWhatsAppNotifications.setEnabled(True)

    def validate(self):
        """Method to validate form data."""

        if (self.ui.lineEdit_accessToken.text() and self.ui.lineEdit_phoneID.text() and
                self.ui.textEdit_recipientsNumbers.toPlainText().strip()):
            self.ui.label_errorMessage.setText("")
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            self.ui.pushButton_testMessage.setEnabled(True)
        else:
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            self.ui.pushButton_testMessage.setEnabled(False)

    def accept_and_close(self):
        """When Ok is clicked, save email config info before closing."""
        self.accept()
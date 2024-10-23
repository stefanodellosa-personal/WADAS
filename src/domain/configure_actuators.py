"""Configure actuators module"""

import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QDialogButtonBox

from ui.ui_configure_actuators import Ui_DialogConfigureActuators


class DialogConfigureActuators(QDialog, Ui_DialogConfigureActuators):
    """Class to instantiate UI dialog to configure actuator server and client(s) parameters."""

    def __init__(self):
        super(DialogConfigureActuators, self).__init__()
        self.ui = Ui_DialogConfigureActuators()

        # UI
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), "img", "mainwindow_icon.jpg")))
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.label_status.setStyleSheet("color: red")

    def validate(self):
        """Method to validate dialog input fields"""

    def accept_and_close(self):
        """When Ok is clicked, save Ai model config info before closing."""

        # TODO: fill up logic
        self.accept()

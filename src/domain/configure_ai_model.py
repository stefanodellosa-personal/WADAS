"""Configure Ai model module."""


import os

from PySide6.QtWidgets import QDialog, QDialogButtonBox
from PySide6.QtGui import QIcon

from ui.ui_configure_ai_model import Ui_DialogConfigureAi
from domain.ai_model import AiModel

class ConfigureAiModel(QDialog, Ui_DialogConfigureAi):
    """Class to instantiate UI dialog to configure Ai model parameters."""

    def __init__(self):
        super(ConfigureAiModel, self).__init__()
        self.ui = Ui_DialogConfigureAi()

        # UI
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(
            os.getcwd(), "src", "img","mainwindow_icon.jpg")))
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.label_errorMEssage.setStyleSheet("color: red")
        self.ui.lineEdit_classificationTreshold.setText(str(AiModel.classification_treshold))
        self.ui.lineEdit_detectionTreshold.setText(str(AiModel.detection_treshold))

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)
        self.ui.lineEdit_classificationTreshold.textChanged.connect(self.validate_data)
        self.ui.lineEdit_detectionTreshold.textChanged.connect(self.validate_data)

        self.validate_data()

    def validate_data(self):
        """Method to validate input values."""

        valid = True
        if ((ctreshold := float(self.ui.lineEdit_classificationTreshold.text())) > 1 or
             ctreshold < 0):
            self.ui.label_errorMEssage.setText(
                "Invalid classification treshold. Please insert a value between 0 and 1.")
            valid = False
        elif (dtreshold := float(self.ui.lineEdit_detectionTreshold.text())) > 1 or dtreshold < 0:
            self.ui.label_errorMEssage.setText(
                "Invalid detection treshold. Please insert a value between 0 and 1.")
            valid = False
        else:
            self.ui.label_errorMEssage.setText("")
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(valid)

    def accept_and_close(self):
        """When Ok is clicked, save Ai model config info before closing."""

        AiModel.classification_treshold = float(self.ui.lineEdit_classificationTreshold.text())
        AiModel.detection_treshold = float(self.ui.lineEdit_detectionTreshold.text())

        self.accept()


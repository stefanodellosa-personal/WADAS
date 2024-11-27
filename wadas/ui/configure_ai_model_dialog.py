"""Configure Ai model module."""


import os
import openvino as ov

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QDialogButtonBox

from wadas.ai.models import txt_animalclasses
from wadas.domain.ai_model import AiModel
from wadas.ui.qt.ui_configure_ai_model import Ui_DialogConfigureAi

module_dir_path = os.path.dirname(os.path.abspath(__file__))


class ConfigureAiModel(QDialog, Ui_DialogConfigureAi):
    """Class to instantiate UI dialog to configure Ai model parameters."""

    def __init__(self):
        super(ConfigureAiModel, self).__init__()
        self.ui = Ui_DialogConfigureAi()

        # UI
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(module_dir_path, "..", "img", "mainwindow_icon.jpg")))
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.label_errorMEssage.setStyleSheet("color: red")
        self.ui.lineEdit_classificationTreshold.setText(str(AiModel.classification_threshold))
        self.ui.lineEdit_detectionTreshold.setText(str(AiModel.detection_threshold))
        self.populate_language_dropdown()

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)
        self.ui.lineEdit_classificationTreshold.textChanged.connect(self.validate_data)
        self.ui.lineEdit_detectionTreshold.textChanged.connect(self.validate_data)

        self.validate_data()
        self.available_ai_devices = ov.Core().get_available_devices()
        self.available_ai_devices.append("auto")
        self.populate_ai_devices_dropdowns()

    def populate_language_dropdown(self):
        """Populate the dropdown with the list of available actuators."""
        self.ui.comboBox_class_lang.clear()
        for language in txt_animalclasses:
            self.ui.comboBox_class_lang.addItem(language)
        if AiModel.language in txt_animalclasses:
            self.ui.comboBox_class_lang.setCurrentText(AiModel.language)

    def populate_ai_devices_dropdowns(self):
        """Method to populate Ai devices list dropdowns."""

        self.ui.comboBox_detection_dev.clear()
        self.ui.comboBox_class_dev.clear()

        for device in self.available_ai_devices:
            self.ui.comboBox_detection_dev.addItem(device)
            self.ui.comboBox_class_dev.addItem(device)
        if AiModel.detection_device in self.available_ai_devices:
            self.ui.comboBox_detection_dev.setCurrentText(AiModel.detection_device)
        else:
            self.ui.comboBox_detection_dev.setCurrentText("auto")
        if AiModel.classification_device in self.available_ai_devices:
            self.ui.comboBox_class_dev.setCurrentText(AiModel.classification_device)
        else:
            self.ui.comboBox_detection_dev.setCurrentText("auto")

    def validate_data(self):
        """Method to validate input values."""

        valid = True
        if (
            ctreshold := float(self.ui.lineEdit_classificationTreshold.text())
        ) > 1 or ctreshold < 0:
            self.ui.label_errorMEssage.setText(
                "Invalid classification treshold. Please insert a value between 0 and 1."
            )
            valid = False
        elif (dtreshold := float(self.ui.lineEdit_detectionTreshold.text())) > 1 or dtreshold < 0:
            self.ui.label_errorMEssage.setText(
                "Invalid detection treshold. Please insert a value between 0 and 1."
            )
            valid = False
        else:
            self.ui.label_errorMEssage.setText("")
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(valid)

    def accept_and_close(self):
        """When Ok is clicked, save Ai model config info before closing."""

        AiModel.classification_threshold = float(self.ui.lineEdit_classificationTreshold.text())
        AiModel.detection_threshold = float(self.ui.lineEdit_detectionTreshold.text())
        AiModel.language = self.ui.comboBox_class_lang.currentText()
        AiModel.detection_device = self.ui.comboBox_detection_dev.currentText()
        AiModel.classification_device = self.ui.comboBox_class_dev.currentText()

        self.accept()

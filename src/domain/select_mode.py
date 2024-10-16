"""Module containing SelectModeDialog custom logic (non autogenerated UI logic)"""

import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog

from domain.operation_mode import OperationMode
from ui.ui_select_mode import Ui_DialogSelectMode


class DialogSelectMode(QDialog, Ui_DialogSelectMode):
    """Dialog to select WADAS operating mode."""

    def __init__(self, selected_mode):
        super(DialogSelectMode, self).__init__()
        self.ui = Ui_DialogSelectMode()
        self.ui.setupUi(self)
        self.setWindowIcon(
            QIcon(os.path.join(os.getcwd(), "img", "mainwindow_icon.jpg"))
        )
        self.selected_mode = selected_mode

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)

        self.initialize_radiobutton_selection()

    def initialize_radiobutton_selection(self):
        """Method to initialize radiobuttons according to previous selection (if any)."""

        if self.selected_mode == OperationMode.OperationModeTypes.AnimalDetectionMode:
            self.ui.radioButton_animal_det_mode.setChecked(True)
        elif (
            self.selected_mode
            == OperationMode.OperationModeTypes.AnimalDetectionAndClassificationMode
        ):
            self.ui.radioButton_animal_det_and_class_mode.setChecked(True)
        elif self.selected_mode == OperationMode.OperationModeTypes.TunnelMode:
            self.ui.radioButton_tunnel_mode.setChecked(True)
        elif self.selected_mode == OperationMode.OperationModeTypes.BearDetectionMode:
            self.ui.radioButton_bear_det_mode.setChecked(True)
        else:
            self.ui.radioButton_test_model_mode.setChecked(True)

    def accept_and_close(self):
        """When Ok is clicked, save radio button selection before closing."""

        if self.ui.radioButton_test_model_mode.isChecked():
            self.selected_mode = OperationMode.OperationModeTypes.TestModelMode
        elif self.ui.radioButton_animal_det_mode.isChecked():
            self.selected_mode = OperationMode.OperationModeTypes.AnimalDetectionMode
        elif self.ui.radioButton_animal_det_and_class_mode.isChecked():
            self.selected_mode = (
                OperationMode.OperationModeTypes.AnimalDetectionAndClassificationMode
            )
        elif self.ui.radioButton_tunnel_mode.isChecked():
            self.selected_mode = OperationMode.OperationModeTypes.TunnelMode
        elif self.ui.radioButton_bear_det_mode.isChecked():
            self.selected_mode = OperationMode.OperationModeTypes.BearDetectionMode
        self.accept()

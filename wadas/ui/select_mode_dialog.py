"""Module containing SelectModeDialog custom logic (non autogenerated UI logic)"""

import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog

from wadas.domain.operation_mode import OperationMode
from wadas.domain.animal_detection_mode import AnimalDetectionAndClassificationMode
from wadas.domain.test_model_mode import TestModelMode
from wadas.ui.qt.ui_select_mode import Ui_DialogSelectMode

module_dir_path = os.path.dirname(os.path.abspath(__file__))


class DialogSelectMode(QDialog, Ui_DialogSelectMode):
    """Dialog to select WADAS operating mode."""

    def __init__(self):
        super(DialogSelectMode, self).__init__()
        self.ui = Ui_DialogSelectMode()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(module_dir_path, "..", "img", "mainwindow_icon.jpg")))

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)

        self.initialize_radiobutton_selection()

    def initialize_radiobutton_selection(self):
        """Method to initialize radiobuttons according to previous selection (if any)."""

        if OperationMode.cur_operation_mode == OperationMode.OperationModeTypes.AnimalDetectionMode:
            self.ui.radioButton_animal_det_mode.setChecked(True)
        elif (
            OperationMode.cur_operation_mode
            == OperationMode.OperationModeTypes.AnimalDetectionAndClassificationMode
        ):
            self.ui.radioButton_animal_det_and_class_mode.setChecked(True)
        elif OperationMode.cur_operation_mode == OperationMode.OperationModeTypes.TunnelMode:
            self.ui.radioButton_tunnel_mode.setChecked(True)
        elif OperationMode.cur_operation_mode == OperationMode.OperationModeTypes.BearDetectionMode:
            self.ui.radioButton_bear_det_mode.setChecked(True)
        else:
            self.ui.radioButton_test_model_mode.setChecked(True)

    def accept_and_close(self):
        """When Ok is clicked, save radio button selection before closing."""

        if self.ui.radioButton_test_model_mode.isChecked():
            OperationMode.cur_operation_mode = TestModelMode()
        elif self.ui.radioButton_animal_det_mode.isChecked():
            OperationMode.cur_operation_mode = AnimalDetectionAndClassificationMode(classification=False)
        elif self.ui.radioButton_animal_det_and_class_mode.isChecked():
            OperationMode.cur_operation_mode = AnimalDetectionAndClassificationMode()
        self.accept()

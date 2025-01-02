# This file is part of WADAS project.
#
# WADAS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WADAS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WADAS. If not, see <https://www.gnu.org/licenses/>.
#
# Author(s): Stefano Dell'Osa, Alessandro Palla, Cesare Di Mauro, Antonio Farina
# Date: 2024-08-16
# Description: Module containing SelectModeDialog custom logic (non autogenerated UI logic)

import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog

from wadas.ai.models import txt_animalclasses
from wadas.domain.ai_model import AiModel
from wadas.domain.operation_mode import OperationMode
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
        self.ui.radioButton_custom_species_class_mode.clicked.connect(self.enable_species_selection)
        self.ui.radioButton_tunnel_mode.clicked.connect(self.disable_species_selection)
        self.ui.radioButton_bear_det_mode.clicked.connect(self.disable_species_selection)
        self.ui.radioButton_animal_det_mode.clicked.connect(self.disable_species_selection)
        self.ui.radioButton_animal_det_and_class_mode.clicked.connect(self.disable_species_selection)

        self.selected_species = None

        self.populate_species_dropdown()
        self.initialize_radiobutton_selection()

    def initialize_radiobutton_selection(self):
        """Method to initialize radiobuttons according to previous selection (if any)."""

        # Set default selection
        self.ui.radioButton_test_model_mode.setChecked(True)
        self.disable_species_selection()

        if OperationMode.cur_operation_mode_type and OperationMode.cur_operation_mode_type.value:
            match OperationMode.cur_operation_mode_type:
                case OperationMode.OperationModeTypes.AnimalDetectionMode:
                    self.ui.radioButton_animal_det_mode.setChecked(True)
                case OperationMode.OperationModeTypes.AnimalDetectionAndClassificationMode:
                    self.ui.radioButton_animal_det_and_class_mode.setChecked(True)
                case OperationMode.OperationModeTypes.TunnelMode:
                    self.ui.radioButton_tunnel_mode.setChecked(True)
                case OperationMode.OperationModeTypes.BearDetectionMode:
                    self.ui.radioButton_bear_det_mode.setChecked(True)
                case OperationMode.OperationModeTypes.CustomSpeciesClassificationMode:
                    self.ui.radioButton_custom_species_class_mode.setChecked(True)
                    self.enable_species_selection()
                    if (OperationMode.cur_custom_classification_species and
                            OperationMode.cur_custom_classification_species in txt_animalclasses[AiModel.language]):
                      self.ui.comboBox_select_species.setCurrentText(OperationMode.cur_custom_classification_species)

    def accept_and_close(self):
        """When Ok is clicked, save radio button selection before closing."""

        if self.ui.radioButton_test_model_mode.isChecked():
            OperationMode.cur_operation_mode_type = OperationMode.OperationModeTypes.TestModelMode
        elif self.ui.radioButton_animal_det_mode.isChecked():
            OperationMode.cur_operation_mode_type = OperationMode.OperationModeTypes.AnimalDetectionMode
        elif self.ui.radioButton_animal_det_and_class_mode.isChecked():
            OperationMode.cur_operation_mode_type = OperationMode.OperationModeTypes.AnimalDetectionAndClassificationMode
        elif self.ui.radioButton_bear_det_mode.isChecked():
            OperationMode.cur_operation_mode_type = OperationMode.OperationModeTypes.BearDetectionMode
        elif self.ui.radioButton_custom_species_class_mode.isChecked():
            OperationMode.cur_operation_mode_type = OperationMode.OperationModeTypes.CustomSpeciesClassificationMode
            OperationMode.cur_custom_classification_species = self.ui.comboBox_select_species.currentText()

        self.accept()

    def populate_species_dropdown(self):
        """Populate the dropdown with the list of available actuators."""
        self.ui.comboBox_select_species.clear()
        for species in txt_animalclasses[AiModel.language]:
            self.ui.comboBox_select_species.addItem(species)

    def enable_species_selection(self):
        """Method to enable/disabled UI widgets related to the custom species selection"""
        self.ui.comboBox_select_species.setEnabled(True)

    def disable_species_selection(self):
        """Method to enable/disabled UI widgets related to the custom species selection"""
        self.ui.comboBox_select_species.setEnabled(False)

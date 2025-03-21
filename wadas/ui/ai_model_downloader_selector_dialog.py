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
# Date: 2025-01-01
# Description: Module containing Ai Model downloader selector class and methods.

import os
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QGroupBox,
    QVBoxLayout,
    QCheckBox,
    QScrollArea,
    QDialogButtonBox,
)

module_dir_path = os.path.dirname(os.path.abspath(__file__))

class Dialog_AiModelDownloaderSelector(QDialog):
    """Class to implement AI model downloader selector dialog."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select AI Models to download")
        self.setWindowIcon(QIcon(os.path.join(module_dir_path, "..", "img", "mainwindow_icon.jpg")))

        main_layout = QVBoxLayout(self)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        groupBox_detection = QGroupBox("Detection models", self)
        vertical_layout_detection = QVBoxLayout(groupBox_detection)

        detection_models = ["Model 1", "Model 2", "Model 3"] #TODO: add logic to fetch list from hf
        for model in detection_models:
            checkbox = QCheckBox(model, self)
            vertical_layout_detection.addWidget(checkbox)

        scroll_area_detection = QScrollArea(self)
        scroll_area_detection.setWidgetResizable(True)
        scroll_area_detection.setWidget(groupBox_detection)


        groupBox_classification = QGroupBox("Classification models", self)
        vertical_layout_classification = QVBoxLayout(groupBox_classification)


        classification_models = ["Model A", "Model B", "Model C"] #TODO: add logic to fetch list from hf
        for model in classification_models:
            checkbox = QCheckBox(model, self)
            vertical_layout_classification.addWidget(checkbox)

        scroll_area_classification = QScrollArea(self)
        scroll_area_classification.setWidgetResizable(True)
        scroll_area_classification.setWidget(groupBox_classification)

        main_layout.addWidget(scroll_area_detection)
        main_layout.addWidget(scroll_area_classification)

        main_layout.addWidget(self.buttonBox)

    def accept(self):
        """"""
        selected_detection_models = []
        selected_classification_models = []

        for checkbox in self.findChildren(QCheckBox):
            if "Detection" in checkbox.parent().title() and checkbox.isChecked():
                selected_detection_models.append(checkbox.text())

            if "Classification" in checkbox.parent().title() and checkbox.isChecked():
                selected_classification_models.append(checkbox.text())

        super().accept()

    def reject(self):
        """"""
        super().reject()





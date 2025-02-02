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
# Date: 2024-10-01
# Description: Web interface users UI Module

import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QScrollArea,
    QWidget,
)


from wadas.domain.database import DataBase
from wadas.ui.qt.ui_configure_web_interface import Ui_DialogConfigureWebInterface

module_dir_path = os.path.dirname(os.path.abspath(__file__))

class DialogConfigureWebInterface(QDialog, Ui_DialogConfigureWebInterface):
    """Class to configure FTP server and cameras"""

    def __init__(self):
        super(DialogConfigureWebInterface, self).__init__()
        self.ui = Ui_DialogConfigureWebInterface()
        self.ui_user_idx = 0
        self.removed_users = []
        self.removed_rows = set()

        # UI
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(module_dir_path, "..", "img", "mainwindow_icon.jpg")))
        self.ui.pushButton_remove_user.setEnabled(False)
        self.ui.pushButton_reset_password.setEnabled(False)
        self.ui.label_errorMessage.setStyleSheet("color: red")

        # Create scrollable area for ftp camera list in FTPCamera tab
        scroll_area = QScrollArea(self.ui.verticalLayoutWidget)
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        users_grid_layout = QGridLayout(scroll_widget)
        users_grid_layout.setObjectName("gridLayout_users")
        self.ui.verticalLayout_users.addWidget(scroll_area)
        # Adding first row of camera form
        self.add_user()

        # Slots
        self.ui.buttonBox.button(QDialogButtonBox.Close).clicked.connect(self.close)
        self.ui.pushButton_add_user.clicked.connect(self.add_user)
        self.ui.pushButton_remove_user.clicked.connect(self.remove_user)
        self.ui.pushButton_reset_password.clicked.connect(self.reset_user_password)

        # Init dialog
        self.initialize_dialog()

        # DB enablement status
        self.db_enabled = bool(DataBase.get_enabled_db())

    def initialize_dialog(self):
        """Method to initialize dialog with existing values (if any)."""

        #TODO: add query to init users list
        pass

    def add_user(self):
        """Method to add a user into the dialog"""

        grid_layout_users = self.findChild(QGridLayout, "gridLayout_users")
        if grid_layout_users:
            row = self.ui_user_idx
            # User selection check box
            radio_button = QRadioButton()
            radio_button.setObjectName(f"radioButton_user_{row}")
            radio_button.setChecked(False)
            radio_button.clicked.connect(self.on_radio_button_clicked)
            grid_layout_users.addWidget(radio_button, row, 0)
            # User
            label = QLabel("User:")
            label.setObjectName(f"label_user_{row}")
            grid_layout_users.addWidget(label, row, 1)
            user_line_edit = QLineEdit()
            user_line_edit.setObjectName(f"lineEdit_user_{row}")
            user_line_edit.textChanged.connect(self.validate)
            grid_layout_users.addWidget(user_line_edit, row, 2)

            grid_layout_users.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.ui_user_idx += 1

            self.validate()

    def remove_user(self):
        """Method to remove user from list."""

        for i in range(0, self.ui_user_idx):
            radiobtn = self.findChild(QRadioButton, f"radioButton_user_{i}")
            if radiobtn:
                user_ln = self.findChild(QLineEdit, f"lineEdit_user_{i}")
                if radiobtn.isChecked() and user_ln:
                    self.removed_users.append(user_ln.text())
                    self.removed_rows.add(i)
                    grid_layout_users = self.findChild(QGridLayout, "gridLayout_users")
                    if grid_layout_users:
                        for j in range(0, 3):
                            grid_layout_users.itemAtPosition(i, j).widget().setParent(None)
        self.ui.pushButton_remove_user.setEnabled(False)
        self.ui.pushButton_reset_password.setEnabled(False)

    def on_radio_button_clicked(self):
        """Method to update remove user button enablement logic."""

        self.ui.pushButton_remove_user.setEnabled(True)
        self.ui.pushButton_reset_password.setEnabled(True)

    def validate(self):
        """Method to validate dialog input fields"""

        #TODO: add form validation logic
        pass

    def reset_user_password(self):
        """Method to reset user password in db."""

        #TODO: add logic
        pass

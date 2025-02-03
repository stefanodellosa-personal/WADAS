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
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QScrollArea,
    QWidget,
)
from sqlalchemy import select

from wadas.domain.database import DataBase
from wadas.domain.db_model import User
from wadas.ui.qt.ui_configure_web_interface import Ui_DialogConfigureWebInterface
from wadas.ui.error_message_dialog import WADASErrorMessage

module_dir_path = os.path.dirname(os.path.abspath(__file__))

class DialogConfigureWebInterface(QDialog, Ui_DialogConfigureWebInterface):
    """Class to configure FTP server and cameras"""

    def __init__(self):
        super(DialogConfigureWebInterface, self).__init__()
        self.ui = Ui_DialogConfigureWebInterface()
        self.ui_user_idx = 0
        self.removed_users = []
        self.removed_rows = set()
        # DB enablement status
        self.db_enabled = bool(DataBase.get_enabled_db())

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
        self.ui.buttonBox.accepted.connect(self.accept_and_close)
        self.ui.pushButton_add_user.clicked.connect(self.add_user)
        self.ui.pushButton_remove_user.clicked.connect(self.remove_user)
        self.ui.pushButton_reset_password.clicked.connect(self.reset_user_password)

        # Init dialog
        self.initialize_dialog()

    def initialize_dialog(self):
        """Method to initialize dialog with existing values (if any)."""

        if self.db_enabled:
            i = 0
            try:
                if session := DataBase.create_session():
                    stmt = select(User.username)
                    for username in session.scalars(stmt):
                        if i > 0:
                            self.add_user()
                        user_ln = self.findChild(QLineEdit, f"lineEdit_user_{i}")
                        user_ln.setText(username)
                        password_ln = self.findChild(QLineEdit, f"lineEdit_password_{i}")
                        password_ln.setText("xxxxxxx")
                        password_ln.setEnabled(False)
                    self.validate()
                else:
                    return None
            except:
                WADASErrorMessage("Failed to retrieve users data",
                                  "Failed to retrieve user data from db. "
                                  "Please make sure db is healty and properly configured.")

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
            # Password
            label = QLabel("Password:")
            label.setObjectName(f"label_password_{row}")
            grid_layout_users.addWidget(label, row, 3)
            pass_line_edit = QLineEdit()
            pass_line_edit.setObjectName(f"lineEdit_password_{row}")
            pass_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
            pass_line_edit.textChanged.connect(self.validate)
            grid_layout_users.addWidget(pass_line_edit, row, 4)

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
                        for j in range(0, 5):
                            grid_layout_users.itemAtPosition(i, j).widget().setParent(None)
        self.ui.pushButton_remove_user.setEnabled(False)
        self.ui.pushButton_reset_password.setEnabled(False)

    def on_radio_button_clicked(self):
        """Method to update remove user button enablement logic."""

        self.ui.pushButton_remove_user.setEnabled(True)
        self.ui.pushButton_reset_password.setEnabled(True)

    def get_user(self, row):
        """Method to get user text from UI programmatically by row number"""
        userln = self.findChild(QLineEdit, f"lineEdit_user_{row}")
        return userln.text() if userln else None

    def get_password(self, row):
        """Method to get user password text from UI programmatically by row number"""
        password_ln = self.findChild(QLineEdit, f"lineEdit_password_{row}")
        return password_ln.text() if password_ln else False

    def validate(self):
        """Method to validate dialog input fields"""

        for i in range(0, self.ui_user_idx):
            if i in self.removed_rows:
                continue
            if not self.get_user(i):
                self.ui.label_errorMessage.setText("Invalid user name provided!")
                return False
            if not self.get_password(i):
                self.ui.label_errorMessage.setText("Invalid user name provided!")
                return False

        self.ui.label_errorMessage.setText("")
        return True


    def reset_user_password(self):
        """Method to reset user password in db."""

        for i in range(0, self.ui_user_idx):
            radiobtn = self.findChild(QRadioButton, f"radioButton_user_{i}")
            if radiobtn:
                user_ln = self.findChild(QLineEdit, f"lineEdit_password_{i}")
                if radiobtn.isChecked():
                    user_ln.Enabled(True)

    def accept_and_close(self):
        """Method to apply changes to db"""

        self.close()

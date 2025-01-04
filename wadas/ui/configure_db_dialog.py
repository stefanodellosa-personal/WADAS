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
# Date: 2024-08-14
# Description: DB UI configuration module.

import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QDialogButtonBox

from domain.database import SQLiteDataBase, MySQLDataBase
from wadas.domain.database import DataBase, DBTypes
from wadas.ui.qt.ui_configure_db_dialog import Ui_ConfigureDBDialog

module_dir_path = os.path.dirname(os.path.abspath(__file__))

class ConfigureDBDialog(QDialog, Ui_ConfigureDBDialog):
    """Class to insert DB configuration to enable WADAS for database persistency."""

    def __init__(self):
        super(ConfigureDBDialog, self).__init__()
        self.ui = Ui_ConfigureDBDialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(module_dir_path, "..", "img", "mainwindow_icon.jpg")))
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.label_error.setStyleSheet("color: red")
        self.ui.pushButton_test_db.setEnabled(False)

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)
        self.ui.pushButton_create_db.clicked.connect(self.create_db)
        self.ui.pushButton_test_db.clicked.connect(self.test_db)
        self.ui.radioButton_MySQL.clicked.connect(self.on_radioButton_checked)
        self.ui.radioButton_SQLite.clicked.connect(self.on_radioButton_checked)
        self.ui.lineEdit_db_host.textChanged.connect(self.validate)
        self.ui.lineEdit_db_username.textChanged.connect(self.validate)
        self.ui.lineEdit_db_password.textChanged.connect(self.validate)

        self.init_dialog()

    def init_dialog(self):
        """Method to initialize dialog with saved configuration data"""

        if not DataBase.WADAS_DB:
            self.ui.checkBox.setChecked(True)
            self.ui.radioButton_SQLite.setChecked(True)
        else:
            self.ui.checkBox.setChecked(DataBase.WADAS_DB.enabled)
            self.ui.lineEdit_db_host.setText(DataBase.WADAS_DB.host)
            print(f"WADAS_DB: {DataBase.WADAS_DB}, type: {type(DataBase.WADAS_DB)}")
            print(f"DBTypes.MYSQL.__module__: {DBTypes.MYSQL.__module__}")
            print(f"DataBase.WADAS_DB.db_type.__module__: {DataBase.WADAS_DB.db_type.__module__}")
            print(f"db_type: {DataBase.WADAS_DB.db_type}, type: {type(DataBase.WADAS_DB.db_type)}")
            print(f"DBTypes.MYSQL: {DBTypes.MYSQL}, type: {type(DBTypes.MYSQL)}")
            if DataBase.WADAS_DB.db_type == DBTypes.MYSQL:
                self.ui.radioButton_MySQL.setChecked(True)
                self.ui.lineEdit_db_username.setText(DataBase.WADAS_DB.username)
                self.ui.lineEdit_db_name.setText(DataBase.WADAS_DB.database_name)
            else:
                self.ui.radioButton_SQLite.setChecked(True)
        self.on_radioButton_checked()

    def on_radioButton_checked(self):
        """Method to update dialog fields depending on DB selection"""

        self.ui.lineEdit_db_username.setEnabled(not self.ui.radioButton_SQLite.isChecked())
        self.ui.lineEdit_db_password.setEnabled(not self.ui.radioButton_SQLite.isChecked())
        self.ui.lineEdit_db_name.setEnabled(not self.ui.radioButton_SQLite.isChecked())

    def _update_common_params(self):
        DataBase.WADAS_DB.host = self.ui.lineEdit_db_host.text()
        DataBase.WADAS_DB.enabled = self.ui.checkBox.isChecked()

    def _update_mysql_params(self):
        self._update_common_params()
        DataBase.WADAS_DB.username = self.ui.lineEdit_db_username.text()
        DataBase.WADAS_DB.database_name = self.ui.lineEdit_db_name.text()

    def accept_and_close(self):
        """When Ok is clicked, save db config info before closing."""
        if self.ui.radioButton_SQLite.isChecked():
            if not DataBase.WADAS_DB or DataBase.WADAS_DB.db_type != DBTypes.SQLITE:
                self.new_sqlite_db()
            else:
                self._update_common_params()
        else:
            if not DataBase.WADAS_DB or DataBase.WADAS_DB.db_type != DBTypes.MYSQL:
                self.new_mysql_db()
            else:
                self._update_mysql_params()

        self.accept()

    def new_mysql_db(self):
        """Method to create new MySQL DB with dialog input fields"""
        DataBase.WADAS_DB = MySQLDataBase(self.ui.lineEdit_db_host.text(),
                                          self.ui.lineEdit_db_username.text(),
                                          self.ui.lineEdit_db_name.text(),
                                          self.ui.checkBox.isChecked())

    def new_sqlite_db(self):
        """Method to create new SQLite DB with dialog input fields"""

        DataBase.WADAS_DB = SQLiteDataBase(self.ui.lineEdit_db_host.text(), self.ui.checkBox.isChecked())

    def create_db(self):
        """Method to trigger new db creation"""

        pass #TODO: implement logic and remove

    def validate(self):
        """Method to validate db parameters"""

        valid = True

        if not self.ui.lineEdit_db_host.text():
            self.ui.label_error.setText("Database host field cannot be empty.")
            valid = False

        if self.ui.radioButton_MySQL.isChecked():
            if not self.ui.lineEdit_db_username.text():
                self.ui.label_error.setText("Database username field cannot be empty.")
                valid = False
            if not self.ui.lineEdit_db_password.text():
                self.ui.label_error.setText("Database password field cannot be empty.")
                valid = False

        if valid:
            self.ui.label_error.setText("")
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(valid)
            self.ui.pushButton_test_db.setEnabled(valid)

    def test_db(self):
        """Method to test db connection"""

        pass #TODO: implement logic and remove


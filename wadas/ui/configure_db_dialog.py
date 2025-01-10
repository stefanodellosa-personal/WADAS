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

import keyring
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QMessageBox

from domain.database import MariaDBDataBase
from wadas.domain.actuator import Actuator
from wadas.domain.camera import cameras
from wadas.domain.database import DataBase, SQLiteDataBase, MySQLDataBase
from wadas.ui.error_message_dialog import WADASErrorMessage
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
        self.ui.radioButton_MariaDB.clicked.connect(self.on_radioButton_checked)
        self.ui.lineEdit_db_host.textChanged.connect(self.validate)
        self.ui.lineEdit_db_port.textChanged.connect(self.validate)
        self.ui.lineEdit_db_username.textChanged.connect(self.validate)
        self.ui.lineEdit_db_password.textChanged.connect(self.validate)

        self.init_dialog()

    def init_dialog(self):
        """Method to initialize dialog with saved configuration data"""

        if not (wadas_db := DataBase.get_instance()):
            self.ui.checkBox.setChecked(True)
            self.ui.radioButton_SQLite.setChecked(True)
        else:
            self.ui.checkBox.setChecked(wadas_db.enabled)
            self.ui.lineEdit_db_host.setText(wadas_db.host)
            if wadas_db.type:
                if wadas_db.type == DataBase.DBTypes.MYSQL:
                    self.ui.radioButton_MySQL.setChecked(True)
                    pwd = keyring.get_password("WADAS_DB_MySQL", wadas_db.username)
                    self.ui.lineEdit_db_port.setText(str(wadas_db.port))
                    self.ui.lineEdit_db_username.setText(wadas_db.username)
                    self.ui.lineEdit_db_password.setText(pwd)
                    self.ui.lineEdit_db_name.setText(wadas_db.database_name)
                elif wadas_db.type == DataBase.DBTypes.MARIADB:
                    pwd = keyring.get_password("WADAS_DB_MariaDB", wadas_db.username)
                    self.ui.lineEdit_db_port.setText(str(wadas_db.port))
                    self.ui.lineEdit_db_username.setText(wadas_db.username)
                    self.ui.lineEdit_db_password.setText(pwd)
                    self.ui.lineEdit_db_name.setText(wadas_db.database_name)
                elif wadas_db.type == DataBase.DBTypes.SQLITE:
                    self.ui.radioButton_SQLite.setChecked(True)
                else:
                    unrecognized_db_type_dlg = WADASErrorMessage("Unrecognized DB type",
                                                                 "Database type is not recognized or supported.")
                    unrecognized_db_type_dlg.exec()
            else:
                unrecognized_db_type_dlg = WADASErrorMessage("No DB type",
                                                             "Database type is not configured.")
                unrecognized_db_type_dlg.exec()
        self.on_radioButton_checked()

    def on_radioButton_checked(self):
        """Method to update dialog fields depending on DB selection"""

        auth_db_selected = self.ui.radioButton_MySQL.isChecked() or self.ui.radioButton_MariaDB.isChecked()
        self.ui.lineEdit_db_port.setEnabled(auth_db_selected)
        self.ui.lineEdit_db_username.setEnabled(auth_db_selected)
        self.ui.lineEdit_db_password.setEnabled(auth_db_selected)
        self.ui.lineEdit_db_name.setEnabled(auth_db_selected)
        if auth_db_selected and not self.ui.lineEdit_db_name.text():
            self.ui.lineEdit_db_name.setPlaceholderText("wadas")
        elif self.ui.radioButton_SQLite.isChecked():
            self.ui.lineEdit_db_name.setPlaceholderText("")

    def _update_common_params(self, wadas_db):
        """Method to update params common to MySQL and SQLite db types"""

        wadas_db.host = self.ui.lineEdit_db_host.text()
        wadas_db.enabled = self.ui.checkBox.isChecked()

    def _update_mysql_params(self, wadas_db):
        """Method to update params specific to MySQL or MariaDB db type"""

        self._update_common_params(wadas_db)
        wadas_db.port = int(self.ui.lineEdit_db_port.text())
        wadas_db.username = self.ui.lineEdit_db_username.text()
        wadas_db.database_name = self.ui.lineEdit_db_name.text()

    def accept_and_close(self):
        """When Ok is clicked, save db config info before closing."""

        wadas_db = DataBase.get_instance()
        if self.ui.radioButton_SQLite.isChecked():
            if not wadas_db:
                self.new_sqlite_db()
            elif wadas_db.type != DataBase.DBTypes.SQLITE:
                if self.ask_db_type_change():
                    DataBase.destroy_instance()
                    self.new_sqlite_db()
            else:
                self._update_common_params(wadas_db)
        elif self.ui.radioButton_MySQL.isChecked():
            if not wadas_db:
                self.new_mysql_db()
            elif wadas_db.type != DataBase.DBTypes.MYSQL:
                if self.ask_db_type_change():
                    DataBase.destroy_instance()
                    self.new_mysql_db()
            else:
                self._update_mysql_params(wadas_db)
        elif self.ui.radioButton_MariaDB.isChecked():
            if not wadas_db:
                self.new_mariadb_db()
            elif wadas_db.type != DataBase.DBTypes.MARIADB:
                if self.ask_db_type_change():
                    DataBase.destroy_instance()
                    self.new_mariadb_db()
            else:
                self._update_mysql_params(wadas_db)

        self.accept()

    def ask_db_type_change(self):
        reply = QMessageBox.question(
            self,
            "Confirm Replace Database",
            "Changing the database type will replace the existing database. Do you want to continue?",
            QMessageBox.Yes | QMessageBox.No
        )
        return reply != QMessageBox.No

    def new_mysql_db(self):
        """Method to create and initialize a new MySQL DB with dialog input fields"""
        mysql_db = MySQLDataBase(self.ui.lineEdit_db_host.text(),
                                 int(self.ui.lineEdit_db_port.text()),
                                  self.ui.lineEdit_db_username.text(),
                                  self.ui.lineEdit_db_name.text(),
                                  self.ui.checkBox.isChecked())
        keyring.set_password(
            f"WADAS_DB_MySQL",
            self.ui.lineEdit_db_username.text(),
            self.ui.lineEdit_db_password.text(),
        )
        DataBase.initialize(mysql_db)

    def new_sqlite_db(self):
        """Method to create and initialize a new SQLite DB with dialog input fields"""

        sqlite_db = SQLiteDataBase(self.ui.lineEdit_db_host.text(), self.ui.checkBox.isChecked())
        DataBase.initialize(sqlite_db)

    def new_mariadb_db(self):
        """Method to create and initialize a new MariaDB with dialog input fields"""

        maria_db = MariaDBDataBase(self.ui.lineEdit_db_host.text(),
                                 int(self.ui.lineEdit_db_port.text()),
                                  self.ui.lineEdit_db_username.text(),
                                  self.ui.lineEdit_db_name.text(),
                                  self.ui.checkBox.isChecked())
        keyring.set_password(
            f"WADAS_DB_MariaDB",
            self.ui.lineEdit_db_username.text(),
            self.ui.lineEdit_db_password.text(),
        )
        DataBase.initialize(maria_db)

    def create_db(self):
        """Method to trigger new db creation"""

        if self.ui.radioButton_SQLite.isChecked():
            if not DataBase.get_instance():
                self.new_sqlite_db()
            elif self.ui.radioButton_MySQL.isChecked():
                self.new_mysql_db()
            elif self.ui.radioButton_MariaDB.isChecked():
                self.new_mariadb_db()

        if db := DataBase.get_instance():
            db.create_database()
            # Populate DB with existing cameras and actuators
            if cameras:
                for camera in cameras:
                    db.insert_into_db(camera)
            if Actuator.actuators:
                for actuator_id in Actuator.actuators:
                    db.insert_into_db(Actuator.actuators[actuator_id])
            self.show_create_status(True)
        else:
            self.show_create_status(False)

        DataBase.destroy_instance()

    def show_create_status(self, success: bool):
        """Method to show message with db creation status"""

        message = "Database successfully created!" if success else "Failed to create the db!"
        icon = QMessageBox.Information if success else QMessageBox.Critical
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Database creation status")
        msg_box.setWindowIcon(QIcon(os.path.join(module_dir_path, "..", "img", "mainwindow_icon.jpg")))
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setStandardButtons(QMessageBox.Ok)

        msg_box.exec()

    def validate_port(self, port):
        """Validate port method"""

        try:
            port_to_int = int(port)
        except  ValueError:
            self.ui.label_error.setText("Invalid port type. Shall be an integer value!")
            return False

        if port_to_int < 1 or port_to_int > 65535:
            self.ui.label_error.setText("Invalid port provided!")
            return False
        else:
            return True

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

            if port := self.ui.lineEdit_db_port.text():
                if not self.validate_port(port):
                    valid = False
            else:
                self.ui.label_error.setText("No server port provided!")
                valid = False

        if valid:
            self.ui.label_error.setText("")
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(valid)
            self.ui.pushButton_test_db.setEnabled(valid)

    def test_db(self):
        """Method to test db connection"""

        pass #TODO: implement logic and remove


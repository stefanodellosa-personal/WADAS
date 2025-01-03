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

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)
        self.ui.pushButton_create_db.clicked.connect(self.create_db)
        self.ui.pushButton_test_db.clicked.connect(self.test_db)

    def init_dialog(self):
        """Method to initialize dialog with saved configuration data"""

        pass #TODO: implement logic and remove

    def accept_and_close(self):
        """When Ok is clicked, save db config info before closing."""

        self.accept()

    def create_db(self):
        """Method to trigger new db creation"""

        pass #TODO: implement logic and remove

    def validate(self):
        """Method to validate db parameters"""

        pass #TODO: implement logic and remove

    def test_db(self):
        """Method to test db connection"""

        pass #TODO: implement logic and remove


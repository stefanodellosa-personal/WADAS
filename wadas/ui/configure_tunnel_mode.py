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
# Description: Configure tunnel mode UI module

from pathlib import Path

from PySide6.QtCore import Qt, QThread
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QLineEdit,
)

from wadas.ui.qt.ui_configure_tunnel_mode import Ui_DialogConfigureTunnelMode

module_dir_path = Path(__file__).parent


class DialogConfigureTunnelMode(QDialog, Ui_DialogConfigureTunnelMode):
    """Class to configure Tunnel mode"""

    def __init__(self):
        super(DialogConfigureTunnelMode, self).__init__()
        self.ui = Ui_DialogConfigureTunnelMode()

        # UI
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(str(module_dir_path.parent / "img" / "mainwindow_icon.jpg")))

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)


    def accept_and_close(self):
        """Method to apply changed before closing dialog."""
        self.accept()
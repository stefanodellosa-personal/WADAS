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
# Description: Configure camera for tunnel mode UI module

from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog

from wadas.ai.object_counter import TrackingRegion
from wadas.ui.qt.ui_configure_camera_for_tunnel_mode import Ui_DialogConfigureCameraForTunnelMode

module_dir_path = Path(__file__).parent


class DialogConfigureCameraForTunnelMode(QDialog, Ui_DialogConfigureCameraForTunnelMode):
    """Class to configure camera for Tunnel mode"""

    def __init__(self, direction=None):
        super(DialogConfigureCameraForTunnelMode, self).__init__()
        self.ui = Ui_DialogConfigureCameraForTunnelMode()
        self.direction = direction

        # UI
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(str(module_dir_path.parent / "img" / "mainwindow_icon.jpg")))

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)

        self.initialize_direction_status()

    def initialize_direction_status(self):
        """Initialize direction in UI if provided"""

        match self.direction:
            case TrackingRegion.UP.value:
                self.ui.radioButton_top_frame.setChecked(True)
            case TrackingRegion.DOWN.value:
                self.ui.radioButton_bottom_frame.setChecked(True)
            case TrackingRegion.LEFT.value:
                self.ui.radioButton_left_frame.setChecked(True)
            case TrackingRegion.RIGHT.value:
                self.ui.radioButton_right_frame.setChecked(True)

    def accept_and_close(self):
        """Method to apply changed before closing dialog."""

        if self.ui.radioButton_top_frame.isChecked():
            self.direction = TrackingRegion.UP
        if self.ui.radioButton_bottom_frame.isChecked():
            self.direction = TrackingRegion.DOWN
        if self.ui.radioButton_left_frame.isChecked():
            self.direction = TrackingRegion.LEFT
        if self.ui.radioButton_right_frame.isChecked():
            self.direction = TrackingRegion.RIGHT
        self.accept()
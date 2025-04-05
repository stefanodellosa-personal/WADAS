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

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
)

from wadas.domain.tunnel import Tunnel
from wadas.ui.configure_camera_for_tunnel_mode import DialogConfigureCameraForTunnelMode
from wadas.ui.qt.ui_configure_tunnel import Ui_DialogConfigureTunnel

module_dir_path = Path(__file__).parent


class DialogConfigureTunnel(QDialog, Ui_DialogConfigureTunnel):
    """Class to configure Tunnel mode"""

    def __init__(self, cameras, tunnel=None):
        super(DialogConfigureTunnel, self).__init__()
        self.ui = Ui_DialogConfigureTunnel()

        # UI
        self.ui.setupUi(self)
        title = f"Edit tunnel {tunnel}" if tunnel else "New tunnel"
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(str(module_dir_path.parent / "img" / "mainwindow_icon.jpg")))
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        # Tunnel modifications status
        self.tunnel = tunnel
        self.cameras_not_in_tunnels = cameras

        # Init dialog
        self.initialize_camera1_combobox()
        self.initialize_camera2_combobox()

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)
        self.ui.lineEdit_tunnel_name.textChanged.connect(self.validate)
        self.ui.comboBox_camera_1.currentIndexChanged.connect(self.on_camera1_combobox_idx_changed)
        self.ui.comboBox_camera_1.currentIndexChanged.connect(self.on_camera1_combobox_idx_changed)
        self.ui.pushButton_direction_camera_1.clicked.connect(self.set_camera1_direction)
        self.ui.pushButton_direction_camera_2.clicked.connect(self.set_camera2_direction)

        if self.tunnel:
            self.ui.lineEdit_tunnel_name.setText(tunnel.id)
            self.ui.comboBox_camera_1.setCurrentText(tunnel.camera_entrance_1)
            self.ui.comboBox_camera_2.setCurrentText(tunnel.camera_entrance_2)

    def initialize_camera1_combobox(self):
        """Method to initialize camera list dropdown with available cameras."""

        self.ui.comboBox_camera_1.clear()
        for camera in self.cameras_not_in_tunnels:
            if self.ui.comboBox_camera_2.currentText() != camera:
                self.ui.comboBox_camera_1.addItem(camera)

    def initialize_camera2_combobox(self):
        """Method to initialize camera list dropdown with available cameras."""

        self.ui.comboBox_camera_2.clear()
        for camera in self.cameras_not_in_tunnels:
                if self.ui.comboBox_camera_1.currentText() != camera:
                    self.ui.comboBox_camera_2.addItem(camera)

    def on_camera1_combobox_idx_changed(self):
        """Update camera 2 options when camera 1 changes."""
        self.initialize_camera2_combobox()
        self.validate()

    def on_camera2_combobox_idx_changed(self):
        """Update camera 1 options when camera 2 changes."""
        self.initialize_camera1_combobox()
        self.validate()

    def set_camera1_direction(self):
        """Method to set camera 1 direction"""

        if (dlg := DialogConfigureCameraForTunnelMode(self.ui.label_direction_camera_1.text())).exec():
            self.ui.label_direction_camera_1.setText(dlg.direction.value)
        self.validate()

    def set_camera2_direction(self):
        """Method to set camera 2 direction"""

        if (dlg := DialogConfigureCameraForTunnelMode(self.ui.label_direction_camera_2.text())).exec():
            self.ui.label_direction_camera_2.setText(dlg.direction.value)
        self.validate()

    def validate(self):
        """Method to make sure all input are provided before clicking OK button"""

        valid = (bool(self.ui.lineEdit_tunnel_name.text()) and
                 bool(self.ui.comboBox_camera_1.currentText()) and
                 bool(self.ui.comboBox_camera_2.currentText()) and
                 bool(self.ui.label_direction_camera_1.text()) and
                 bool(self.ui.label_direction_camera_2.text()))
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(valid)

    def accept_and_close(self):
        """Method to apply changed before closing dialog."""

        if self.tunnel:
            # Edit existing tunnel
            self.tunnel.id = self.ui.lineEdit_tunnel_name.text()
            self.tunnel.camera_entrance_1 = self.ui.comboBox_camera_1.currentText()
            self.tunnel.camera_entrance_2 = self.ui.comboBox_camera_2.currentText()
        else:
            self.tunnel = Tunnel(self.ui.lineEdit_tunnel_name.text(),
                                 self.ui.comboBox_camera_1.currentText(),
                                 self.ui.comboBox_camera_2.currentText())
        self.accept()
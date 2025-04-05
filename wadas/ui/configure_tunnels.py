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

from wadas.domain.camera import cameras
from wadas.domain.tunnel import Tunnel
from wadas.ui.configure_tunnel import DialogConfigureTunnel
from wadas.ui.qt.ui_configure_tunnels import Ui_DialogTunnels

module_dir_path = Path(__file__).parent


class DialogConfigureTunnels(QDialog, Ui_DialogTunnels):
    """Class to configure Tunnel mode"""

    def __init__(self):
        super(DialogConfigureTunnels, self).__init__()
        self.ui = Ui_DialogTunnels()

        # UI
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(str(module_dir_path.parent / "img" / "mainwindow_icon.jpg")))

        self.ui.pushButton_edit_tunnel.setEnabled(False)
        self.ui.pushButton_remove_tunnel.setEnabled(False)

        # Tunnel modifications status
        self.local_tunnels = Tunnel.tunnels
        self.cameras_not_in_tunnels = [camera.id for camera in cameras]

        # Signals
        self.ui.pushButton_add_tunnel.clicked.connect(self.on_add_tunnel_clicked)
        self.ui.pushButton_remove_tunnel.clicked.connect(self.on_remove_tunnel_clicked)
        self.ui.pushButton_edit_tunnel.clicked.connect(self.on_edit_tunnel_clicked)
        self.ui.listWidget.itemSelectionChanged.connect(self.on_tunnel_selection_changed)

        #Init dialog
        self.update_tunnels_list()

    def update_cameras_not_in_tunnel(self):
        """Method to build the list of available cameras not already associated with a tunnel"""

        for tunnel in self.local_tunnels:
            if tunnel.camera_entrance_1 in self.cameras_not_in_tunnels:
                self.cameras_not_in_tunnels.remove(tunnel.camera_entrance_1)
            if tunnel.camera_entrance_2 in self.cameras_not_in_tunnels:
                self.cameras_not_in_tunnels.remove(tunnel.camera_entrance_2)

    def update_tunnels_list(self):
        """Method to initialize tunnel combobox with existing tunnel objects"""

        self.ui.listWidget.clear()
        for tunnel in self.local_tunnels:
            self.ui.listWidget.addItem(tunnel.id)

    def on_add_tunnel_clicked(self):
        """Method to handle new tunnel insertion"""

        if (dlg := DialogConfigureTunnel(self.cameras_not_in_tunnels)).exec():
            self.local_tunnels.append(dlg.tunnel)
            self.update_tunnels_list()

    def on_remove_tunnel_clicked(self):
        """Method to remove a tunnel"""

        for tunnel in set(self.local_tunnels):
            if tunnel.id == self.ui.listWidget.currentItem():
                self.local_tunnels.remove(tunnel)

    def on_edit_tunnel_clicked(self):
        """Method to handle tunnel editing"""

        for tunnel in self.local_tunnels:
            if tunnel.id == self.ui.listWidget.currentItem():
                if (dlg := DialogConfigureTunnel(self.cameras_not_in_tunnels, tunnel)).exec():
                    tunnel = dlg.tunnel
                self.update_tunnels_list()
                break

    def on_tunnel_selection_changed(self):
        """Method to handle list item selection"""

        if self.ui.listWidget.currentItem():
            self.ui.pushButton_edit_tunnel.setEnabled(True)
            self.ui.pushButton_remove_tunnel.setEnabled(True)
        else:
            self.ui.pushButton_edit_tunnel.setEnabled(False)
            self.ui.pushButton_remove_tunnel.setEnabled(False)
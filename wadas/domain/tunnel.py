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
# Description: Tunnel base class module

import logging

# from wadas.domain.camera import cameras

logger = logging.getLogger(__name__)


class Tunnel:
    """Class to represent tunnels object."""

    # List of Tunnel objects
    tunnels = []

    def __init__(self, id, camera_entrance_1, camera_entrance_2, enabled=True):
        self.id = id
        self.camera_entrance_1 = camera_entrance_1
        self.camera_entrance_1 = camera_entrance_2
        self.enabled = enabled

    @classmethod
    def add_tunnel(cls):
        """Method to add tunnel into the list"""
        pass

    @classmethod
    def remove_tunnel(cls):
        """Method to remove tunnel from the list"""

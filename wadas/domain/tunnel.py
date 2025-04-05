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
        self.camera_entrance_2 = camera_entrance_2
        self.enabled = enabled

    @classmethod
    def add_tunnel(cls, tunnel, entrance1, entrance2):
        """Method to add tunnel into the list"""
        if not cls.tunnel_exists(tunnel):
            cls.tunnels.append(Tunnel(tunnel, entrance1, entrance2))
            logger.info("%s tunnel added.")
        else:
            logger.error("%s tunnel already exists.")

    @classmethod
    def remove_tunnel(cls, tunnel):
        """Method to remove tunnel from the list"""
        for cur_tunnel in set(cls.tunnels):
            if cur_tunnel.id == tunnel.id:
                cls.tunnels.remove(cur_tunnel)
                logger.info("%s tunnel removed.")

    @classmethod
    def update_tunnel(cls, id, camera1, camera2, enabled=True):
        """Method to update existing tunnel"""

        for cur_tunnel in cls.tunnels:
            if cur_tunnel.id == id:
                cur_tunnel.camera_entrance_1 = camera1
                cur_tunnel.camera_entrance_2 = camera2
                cur_tunnel.enabled = enabled
                return True
        return False

    @classmethod
    def tunnel_exists(cls, tunnel):
        """Method to check whether a tunnel is already in the list"""

        for cur_tunnel in cls.tunnels:
            if cur_tunnel.id == tunnel.id:
                return True
        return False

    def serialize(self):
        """Method to serialize Camera object into file."""

        # TODO: implement logic
        pass

    @staticmethod
    def deserialize(data):
        """Method to deserialize Camera object from file."""

        # TODO: implement logic
        pass

"""FTP Camera module"""

import logging

from wadas.domain.actuator import Actuator
from wadas.domain.camera import Camera

logger = logging.getLogger(__name__)


class FTPCamera(Camera):
    """FTP Camera class, specialization of Camera class."""

    def __init__(self, id, ftp_folder, enabled=True, actuators=None):
        if actuators is None:
            actuators = []
        super().__init__(id, enabled)
        self.type = Camera.CameraTypes.FTP_CAMERA
        self.ftp_folder = ftp_folder
        self.actuators = actuators

    def serialize(self):
        """Method to serialize FTP Camera object into file."""
        actuators = [actuator.id for actuator in self.actuators]
        return {
            "type": self.type.value,
            "id": self.id,
            "enabled": self.enabled,
            "ftp_folder": self.ftp_folder,
            "actuators": actuators,
        }

    @staticmethod
    def deserialize(data):
        """Method to deserialize FTP Camera object from file."""

        actuators = (
            [Actuator.actuators[key] for key in data["actuators"]] if "actuators" in data else []
        )
        return FTPCamera(data["id"], data["ftp_folder"], data["enabled"], actuators)

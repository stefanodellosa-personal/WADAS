"""FTP Camera module"""

import logging

from domain.camera import Camera

logger = logging.getLogger(__name__)


class FTPCamera(Camera):
    """FTP Camera class, specialization of Camera class."""

    def __init__(self, id, ftp_folder, enabled=True):
        super().__init__(id, enabled)
        self.type = Camera.CameraTypes.FTPCamera
        self.ftp_folder = ftp_folder

    def serialize(self):
        """Method to serialize FTP Camera object into file."""
        return {
            "type": self.type.value,
            "id": self.id,
            "enabled": self.enabled,
            "ftp_folder": self.ftp_folder,
        }

    @staticmethod
    def deserialize(data):
        """Method to deserialize FTP Camera object from file."""
        return FTPCamera(data["id"], data["ftp_folder"], data["enabled"])

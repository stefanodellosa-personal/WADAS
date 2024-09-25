"""FTP Camera module"""

import time
import os
import logging
import threading

from src.domain.ai_model import get_timestamp
from src.domain.camera import Camera, img_queue

logger = logging.getLogger(__name__)


class FTPCamera(Camera):
    """FTP Camera class, specialization of Camera class."""

    def __init__(self, id, name = "", enabled = False, ftp_folder):
        super().__init__(id, enabled)
        self.type = Camera.CameraTypes.FTPCamera
        self.name = name
        self.ftp_folder = ftp_folder

    def serialize(self):
        """Method to serialize FTP Camera object into file."""
        return dict(
            type = self.type.value,
            id = self.id,
            name = self.name,
            enabled = self.enabled,
            ftp_folder = self.ftp_folder
        )

    @staticmethod
    def deserialize(data):
        """Method to deserialize FTP Camera object from file."""
        return FTPCamera(data["id"], data["name"], data["enabled"], data["ftp_folder"])

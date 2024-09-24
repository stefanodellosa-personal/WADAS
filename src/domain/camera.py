"""Camera module"""

import logging
from abc import abstractmethod
from enum import Enum
from queue import Queue

logger = logging.getLogger(__name__)
img_queue = Queue()
cameras_list = []


class Camera():
    """Base class of a camera."""

    detection_params = {
            'treshold': 180,
            'min_contour_area': 300,
            'detection_per_second': 1,
            'ms_sample_rate': 1000
        }
    class CameraTypes(Enum):
        USBCamera = "USB Camera"
        FTPCamera = "FTP Camera"

    def __init__(self, id):
        self.type = None
        self.id = id
        self.stop_thread = False

    def detect_new_image_file(self):
        """Method implement filesystem observer to detect new images in selected folder tree.
           Only for ftp server camera notifications."""

        logger.info("Starting filesystem observer for camera %s.", self.id)
        #TODO: implement logic.

    @abstractmethod
    def serialize(self):
        """Method to serialize Camera object into file."""
        pass

    @staticmethod
    def deserialize(data):
        """Method to deserialize Camera object from file."""
        pass
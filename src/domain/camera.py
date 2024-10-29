"""Camera module"""

import logging
from abc import abstractmethod
from enum import Enum
from queue import Queue

logger = logging.getLogger(__name__)
# Queue containing all the images received by Cameras to be processed by AiModel
img_queue = Queue()
# List of Cameras selected by user for image processing
cameras = []


class Camera:
    """Base class of a camera."""

    detection_params = {
        "treshold": 180,
        "min_contour_area": 300,
        "detection_per_second": 1,
        "ms_sample_rate": 1000,
    }

    class CameraTypes(Enum):
        USB_CAMERA = "USB Camera"
        FTP_CAMERA = "FTP Camera"

    def __init__(self, id, enabled=False):
        self.type = None
        self.id = id
        self.enabled = enabled
        self.stop_thread = False
        self.actuators = []

    @abstractmethod
    def serialize(self):
        """Method to serialize Camera object into file."""

    @staticmethod
    def deserialize(data):
        """Method to deserialize Camera object from file."""

"""Camera module"""

import logging
from queue import Queue

logger = logging.getLogger(__name__)
img_queue = Queue()

class Camera():
    """Base class of a camera."""

    detection_params = {
            'treshold': 180,
            'min_contour_area': 500,
            'detection_per_second': 1
        }

    def __init__(self):
        self.index = ""
        self.id = ""
        self.is_enabled = False
        self.en_wadas_motion_detection = False
        self.img_folder = ""

    def detect(self):
        """Method to run motion detection on camera video stream.
           Only for cameras that are note povided with commercial motion detection feature."""

        logger.info("Starting motion detection for camera %s.", self.id)

    def detect_new_image_file(self):
        """Method implement filesystem observer to detect new images in selected folder tree.
           Only for ftp server camera notifications."""
 
        logger.info("Starting filesystem observer for camera %s.", self.id)

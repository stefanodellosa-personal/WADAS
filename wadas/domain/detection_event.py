"""Detection event module."""

import logging

logger = logging.getLogger(__name__)


class DetectionEvent:
    """Class to embed detection event information into a dedicated object."""

    def __init__(
        self,
        camera_id,
        time_stamp,
        detection_img_path,
        detection_accuracy,
        classification=True,
        classification_img_path=None,
        classification_accuracy=0.0,
    ):
        self.camera_id = camera_id
        self.time_stamp = time_stamp
        self.detection_img_path = detection_img_path
        self.detection_accuracy = detection_accuracy
        self.classification = classification
        self.classification_img_path = classification_img_path
        self.classification_accuracy = classification_accuracy

"""Detection event module."""

import logging

logger = logging.getLogger(__name__)


class DetectionEvent:
    """Class to embed detection event information into a dedicated object."""

    def __init__(
        self,
        camera_id,
        time_stamp,
        original_image,
        detection_img_path,
        detected_animals,
        classification=True,
        classification_img_path=None,
        classified_animals=None,
    ):
        self.camera_id = camera_id
        self.time_stamp = time_stamp
        self.original_image = original_image
        self.detection_img_path = detection_img_path
        self.detected_animals = detected_animals
        self.classification = classification
        self.classification_img_path = classification_img_path
        self.classified_animals = classified_animals

"""Custom Classification module."""

import logging
from queue import Empty

from wadas.ai.models import txt_animalclasses
from wadas.domain.ai_model import AiModel
from wadas.domain.animal_detection_mode import AnimalDetectionAndClassificationMode
from wadas.domain.camera import img_queue
from wadas.domain.detection_event import DetectionEvent
from wadas.domain.operation_mode import OperationMode
from wadas.domain.utils import get_timestamp

logger = logging.getLogger(__name__)


class CustomClassificationMode(AnimalDetectionAndClassificationMode):
    """Custom Classification Mode class."""

    def __init__(self):
        super().__init__()
        self.process_queue = True
        self.type = OperationMode.OperationModeTypes.CustomSpeciesClassificationMode
        self.target_animal_label = None

    def set_animal_species(self, target_animal_label):
        """Method to select animal to classify according to Ai model availability"""
        if target_animal_label in txt_animalclasses[AiModel.language]:
            self.target_animal_label = target_animal_label
            logger.debug("%s species selected.", target_animal_label)
            return True
        else:
            logger.error("The specified animal species is not handled by WADAS")
            return False

    def run(self):
        """WADAS custom classification mode"""

        self._initialize_processes()
        self.check_for_termination_requests()

        # Run detection model
        while self.process_queue:
            self.check_for_termination_requests()
            # Get image from motion detection notification
            # Timeout is set to 1 second to avoid blocking the thread
            try:
                cur_img = img_queue.get(timeout=1)
            except Empty:
                cur_img = None

            if cur_img:
                logger.debug("Processing image from motion detection notification...")
                detected_results, detected_img_path = self._detect(cur_img["img"])
                self.check_for_termination_requests()

                if detected_results and detected_img_path:
                    classified_img_path, classified_animals = self._classify(
                        cur_img["img"], detected_results
                    )
                    if classified_img_path:
                        detection_event = DetectionEvent(
                            cur_img["camera_id"],
                            get_timestamp(),
                            cur_img["img"],
                            detected_img_path,
                            detected_results,
                            self.en_classification,
                            classified_img_path,
                            classified_animals,
                        )
                        # Send notification and trigger actuators if the target animal is found
                        if any(
                            x["classification"][0] == self.target_animal_label
                            for x in classified_animals
                        ):
                            # Trigger image update in WADAS mainwindow
                            self.update_image.emit(classified_img_path)
                            self.update_info.emit()
                            message = (
                                f"WADAS has classified '{self.last_classified_animals_str}' "
                                f"animal from camera {cur_img['img_id']}!"
                            )
                            logger.info(message)
                            self.send_notification(detection_event, message)

                            self.actuate(cur_img["img_id"])
                        else:
                            logger.info(
                                "Target animal '%s' not found, found '%s' instead. "
                                "Skipping notification.",
                                self.target_animal_label,
                                self.last_classified_animals_str,
                            )
                    else:
                        logger.info("No animals to classify.")

        self.execution_completed()

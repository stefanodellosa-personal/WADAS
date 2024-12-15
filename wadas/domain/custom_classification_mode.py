"""Custom Classification module."""

import logging
from queue import Empty

from wadas.domain.animal_detection_mode import AnimalDetectionAndClassificationMode
from wadas.domain.camera import img_queue

logger = logging.getLogger(__name__)


class CustomClassificationMode(AnimalDetectionAndClassificationMode):
    """Custom Classification Mode class."""

    def __init__(self, target_animal_label="bear"):
        super().__init__()
        self.process_queue = True
        self.target_animal_label = target_animal_label

    def run(self):
        """WADAS custom classification mode"""

        self._initialize_process()
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
                    # Trigger image update in WADAS mainwindow
                    self.update_image.emit(detected_img_path)
                    self.update_info.emit()

                    classified_img_path, classified_animals = self._classify(
                        cur_img["img"], detected_results
                    )
                    if classified_img_path:
                        # Trigger image update in WADAS mainwindow
                        self.update_image.emit(classified_img_path)
                        self.update_info.emit()
                        message = f"WADAS has classified '{self.last_classified_animals_str}' "
                        message += f"animal from camera {cur_img['img_id']}!"

                        # Send notification and trigger actuators if the target animal is found
                        if any(
                            x["classification"][0] == self.target_animal_label
                            for x in classified_animals
                        ):
                            logger.info(message)
                            self.actuate(cur_img["img_id"])
                            self.send_notification(classified_img_path, message)

                        else:
                            logger.debug("Target animal '%s' not found", self.target_animal_label)

                    else:
                        logger.debug("No results to classify.")

        self.execution_completed()

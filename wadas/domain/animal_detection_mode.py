"""Animal Detection and Classification module."""

import logging
from queue import Empty

from wadas.domain.camera import img_queue
from wadas.domain.operation_mode import OperationMode

logger = logging.getLogger(__name__)


class AnimalDetectionAndClassificationMode(OperationMode):
    """Animal Detection and Classification Mode class."""

    def __init__(self, classification=True):
        super(AnimalDetectionAndClassificationMode, self).__init__()
        self.process_queue = True
        self.en_classification = classification
        self.type = (
            OperationMode.OperationModeTypes.AnimalDetectionAndClassificationMode
            if classification
            else OperationMode.OperationModeTypes.AnimalDetectionMode
        )

    def run(self):
        """WADAS animal detection and classification mode"""

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
                    # Trigger image update in WADAS mainwindow
                    self.update_image.emit(detected_img_path)
                    self.update_info.emit()

                    if self.en_classification:
                        classified_img_path, classified_animals = self._classify(
                            cur_img["img"], detected_results
                        )
                        if classified_img_path:
                            # Trigger image update in WADAS mainwindow
                            self.update_image.emit(classified_img_path)
                            self.update_info.emit()
                            message = (
                                f"WADAS has classified '{self.last_classified_animals_str}' "
                                f"animal from camera {cur_img['img_id']}!"
                            )
                            processed_img_path = classified_img_path
                        else:
                            logger.info("No animals to classify.")
                            message = processed_img_path = ""
                    else:
                        processed_img_path = detected_img_path
                        message = "WADAS has detected an animal from camera %s!" % id
                    # Send notification
                    if message and processed_img_path:
                        self.actuate(cur_img["img_id"])
                        self.send_notification(processed_img_path, message)

        self.execution_completed()

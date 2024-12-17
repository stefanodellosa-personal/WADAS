import logging

from wadas.domain.operation_mode import OperationMode

logger = logging.getLogger(__name__)


class TestModelMode(OperationMode):
    def __init__(self):
        super(TestModelMode, self).__init__()
        self.modename = "test_model_mode"
        self.url = ""
        self.last_classified_animals_str = ""
        self.type = OperationMode.OperationModeTypes.TestModelMode

    def run(self):
        """WADAS test model operation mode"""

        if not self.url:
            logger.error("Invalid URL. Aborting.")
            return

        # Initialize ai model
        self.init_model()

        self.check_for_termination_requests()

        self.run_progress.emit(10)
        # Run detection model
        det_data = self.ai_model.process_image_from_url(self.url, "test_model", True)
        img_path = det_data[0]
        det_results = det_data[1]
        detected_img_path = det_data[2]
        self.last_detection = detected_img_path

        # Check if detection has returned results
        if not detected_img_path or not det_results:
            self.execution_completed()
            return

        # Trigger image update in WADAS mainwindow
        self.update_image.emit(detected_img_path)
        message = "WADAS has detected an animal!"
        self.check_for_termination_requests()

        # Classify if detection has identified animals
        if len(det_results["detections"].xyxy) > 0:
            logger.info("Running classification on detection result(s)...")

            classified_img_path, classified_animals = self._classify(img_path, det_results)
            if classified_img_path:
                # Trigger image update in WADAS mainwindow
                self.update_image.emit(classified_img_path)
                self.update_info.emit()
                message = (
                    f"WADAS has classified '{self.last_classified_animals_str}' "
                    f"animal from camera {img_path}!"
                )
            else:
                logger.info("No animals to classify.")
                message = ""

        # Send notification
        self.send_notification(img_path, message)
        self.execution_completed()

    def check_for_termination_requests(self):
        """Terminate current thread if interrupt request comes from Mainwindow."""

        if self.thread().isInterruptionRequested():
            self.run_finished.emit()
            logger.info("Request to stop received. Aborting...")
            return

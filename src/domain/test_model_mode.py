import logging

from domain.operation_mode import OperationMode

logger = logging.getLogger(__name__)

class TestModelMode(OperationMode):
    def __init__(self):
        super(TestModelMode, self).__init__()
        self.modename = "test_model_mode"
        self.url = ""

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

        # Trigger image update in WADAS mainwindow
        self.update_image.emit(detected_img_path)

        self.check_for_termination_requests()

        # Classify if detection has identified animals
        if len(det_results["detections"].xyxy) > 0:
            logger.info("Running classification on detection result(s)...")
            img_path, classified_animals = self.ai_model.classify(img_path, det_results)
            self.last_classification = img_path

            # Prepare a list of classified animals to print in UI
            for animal in classified_animals:
                last = animal["classification"][0]
                if not self.last_classified_animals:
                    self.last_classified_animals = self.last_classified_animals + last
                else:
                    self.last_classified_animals = self.last_classified_animals +", "+last

            # Trigger image update in WADAS mainwindow
            self.update_image.emit(img_path)
        else:
            logger.debug("No results to classify.")

        # Send notification
        message = "WADAS has classified %s animal!" % self.last_classified_animals, img_path
        self.send_notification(message, img_path)

        self.run_finished.emit()
        logger.info("Done with processing.")

    def check_for_termination_requests(self):
        """Terminate current thread if interrupt request comes from Mainwindow."""

        if self.thread().isInterruptionRequested():
            self.run_finished.emit()
            logger.info("Request to stop received. Aborting...")
            return

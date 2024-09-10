import logging

from domain.operation_mode import OperationMode
from domain.camera import img_queue

logger = logging.getLogger(__name__)

class AnimalDetectionMode(OperationMode):
    def __init__(self):
        super(AnimalDetectionMode, self).__init__()
        self.modename = "animal_detection_mode"
        self.url = ""
        self.process_queue = True

    def run(self):
        """WADAS animal detection mode"""

        # Initialize ai model
        self.init_model()
        self.check_for_termination_requests()

        self.run_progress.emit(10)
        logger.info("Ready for video stream from Camera(s)...")
        # Run detection model
        while self.process_queue:
            if img_queue.not_empty:
                logger.debug("Processing image from motion detection notification...")
                img, id = img_queue.get()
                results, detected_img_path = self.ai_model.process_image(img, id, True)

                self.last_detection = detected_img_path

                # Trigger image update in WADAS mainwindow
                self.update_image.emit(detected_img_path)

                self.check_for_termination_requests()

                # Send notification
                message = "WADAS has detected an animal from camera %s!" % id
                self.send_notification(message, detected_img_path)

        self.run_finished.emit()
        logger.info("Done with processing.")

    def check_for_termination_requests(self):
        """Terminate current thread if interrupt request comes from Mainwindow."""

        if self.thread().isInterruptionRequested():
            self.process_queue = False
            self.run_finished.emit()
            logger.info("Request to stop received. Aborting...")
            return

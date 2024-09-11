import logging
from threading import Thread

from domain.operation_mode import OperationMode
from domain.camera import img_queue
from domain.camera import Camera

logger = logging.getLogger(__name__)

class AnimalDetectionMode(OperationMode):
    def __init__(self):
        super(AnimalDetectionMode, self).__init__()
        self.modename = "animal_detection_mode"
        self.cameras_list = []
        self.camera_thread = []
        self.process_queue = True

    def run(self):
        """WADAS animal detection mode"""

        # Initialize ai model
        self.init_model()
        self.check_for_termination_requests()

        logger.info("Instantiating cameras...")
        camera: Camera
        for camera in self.cameras_list:
            if not camera.is_enabled:
                # We should never be here
                continue
            else:
                # Create thread for motion detection
                logger.debug("Instantiating thread for camera %s", camera.id)
                self.camera_thread.append(camera.run())

        self.run_progress.emit(10)
        logger.info("Ready for video stream from Camera(s)...")
        # Run detection model
        while self.process_queue:
            if img_queue.not_empty:
                logger.debug("Processing image from motion detection notification...")
                cur_img = img_queue.get()
                results, detected_img_path = self.ai_model.process_image(cur_img["img"],
                                                                         cur_img["img_id"],
                                                                         True)

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
            # TODO: add camera threads kill
            self.run_finished.emit()
            logger.info("Request to stop received. Aborting...")
            return

"""Animal Detection and Classification module."""


import logging

from src.domain.operation_mode import OperationMode
from src.domain.camera import img_queue
from src.domain.camera import Camera
from src.domain.camera import cameras

logger = logging.getLogger(__name__)

class AnimalDetectionMode(OperationMode):
    """Animal Detection Mode class."""

    def __init__(self):
        super(AnimalDetectionMode, self).__init__()
        self.modename = "animal_detection_mode"
        self.camera_thread = []
        self.process_queue = True

    def run(self):
        """WADAS animal detection mode"""

        # Initialize ai model
        self.init_model()
        self.check_for_termination_requests()

        logger.info("Instantiating cameras...")
        camera: Camera
        for camera in cameras:
            if not camera.enabled or camera.type != Camera.CameraTypes.USBCamera:
                continue
            else:
                # Create thread for motion detection
                logger.debug("Instantiating thread for camera %s", camera.id)
                camera.stop_thread = False
                self.camera_thread.append(camera.run())

        self.run_progress.emit(10)
        self.check_for_termination_requests()
        logger.info("Ready for video stream from Camera(s)...")
        # Run detection model
        while self.process_queue:
            if img_queue.not_empty:
                logger.debug("Processing image from motion detection notification...")
                cur_img = img_queue.get()
                results, detected_img_path = self.ai_model.process_image(cur_img["img"],
                                                                         True)

                self.last_detection = detected_img_path
                self.check_for_termination_requests()
                if results and detected_img_path:
                    # Trigger image update in WADAS mainwindow
                    self.update_image.emit(detected_img_path)

                    # Send notification
                    message = "WADAS has detected an animal from camera %s!" % id
                    self.send_notification(message, detected_img_path)

        self.execution_completed()

    def check_for_termination_requests(self):
        """Terminate current thread if interrupt request comes from Mainwindow."""

        if self.thread().isInterruptionRequested():
            logger.info("Request to stop received. Aborting...")
            self.process_queue = False
            for camera in cameras:
                if camera.type == Camera.CameraTypes.USBCamera:
                    camera.stop_thread = True
            self.run_finished.emit()
            return

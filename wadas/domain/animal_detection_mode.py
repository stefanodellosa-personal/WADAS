"""Animal Detection and Classification module."""

import logging
from queue import Empty

from wadas.domain.camera import Camera, cameras, img_queue
from wadas.domain.ftps_server import FTPsServer
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

    def _initialize_process(self):
        # Initialize ai model
        self.init_model()
        self.check_for_termination_requests()
        self._initialize_cameras()
        self.start_actuator_server()

    def _initialize_cameras(self):
        logger.info("Instantiating cameras...")
        camera: Camera
        for camera in cameras:
            if camera.enabled:
                if camera.type == Camera.CameraTypes.USB_CAMERA:
                    # Create thread for motion detection
                    logger.info("Instantiating thread for camera %s", camera.id)
                    camera.stop_thread = False
                    self.camera_thread.append(camera.run())
                elif (
                    camera.type == Camera.CameraTypes.FTP_CAMERA
                    and FTPsServer.ftps_server
                    and not self.ftp_thread
                ):
                    logger.info("Instantiating FTPS server...")
                    self.ftp_thread = FTPsServer.ftps_server.run()
        logger.info("Ready for video stream from Camera(s)...")

    def _detect(self, cur_image_path):
        results, detected_img_path = self.ai_model.process_image(cur_image_path, True)
        self.last_detection = detected_img_path
        return results, detected_img_path

    def _format_classified_animals_string(self, classified_animals):
        # Prepare a list of classified animals to print in UI
        if self.last_classified_animals_str:
            self.last_classified_animals_str = ""
        for animal in classified_animals:
            last = animal["classification"][0]
            if not self.last_classified_animals_str:
                self.last_classified_animals_str = self.last_classified_animals_str + last
            else:
                self.last_classified_animals_str = self.last_classified_animals_str + ", " + last

    def _classify(self, cur_image_path, detection_results):
        # Classify if detection has identified animals
        if len(detection_results["detections"].xyxy) > 0:
            logger.info("Running classification on detection result(s)...")
            (
                classified_img_path,
                classified_animals,
            ) = self.ai_model.classify(cur_image_path, detection_results)
            self.last_classification = classified_img_path

            self._format_classified_animals_string(classified_animals)
            return classified_img_path, classified_animals
        return None, None

    def run(self):
        """WADAS animal detection and classification mode"""

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

                    if self.en_classification:
                        classified_img_path, classified_animals = self._classify(
                            cur_img["img"], detected_results
                        )
                        if classified_img_path:
                            # Trigger image update in WADAS mainwindow
                            self.update_image.emit(classified_img_path)
                            self.update_info.emit()
                            message = f"WADAS has classified '{self.last_classified_animals_str}' "
                            message += f"animal from camera {cur_img['img_id']}!"
                            processed_img_path = classified_img_path
                        else:
                            logger.debug("No results to classify.")
                            message = processed_img_path = ""
                    else:
                        processed_img_path = detected_img_path
                        message = "WADAS has detected an animal from camera %s!" % id
                    # Send notification
                    if message and processed_img_path:
                        self.actuate(cur_img["img_id"])
                        self.send_notification(processed_img_path, message)

        self.execution_completed()

    def check_for_termination_requests(self):
        """Terminate current thread if interrupt request comes from Mainwindow."""

        if self.thread().isInterruptionRequested():
            logger.info("Request to stop received. Aborting...")
            # Stop FTPS Server (if running)
            if self.ftp_camera_exist() and self.ftp_thread and FTPsServer.ftps_server:
                FTPsServer.ftps_server.server.close_all()
                FTPsServer.ftps_server.server.close()
                self.ftp_thread.join()
            # Stop USB Cameras thread(s), if any.
            self.process_queue = False
            for camera in cameras:
                if camera.type == Camera.CameraTypes.USB_CAMERA:
                    camera.stop_thread = True

            self.stop_actuator_server()

            self.run_finished.emit()
            return

    def ftp_camera_exist(self):
        for camera in cameras:
            if camera.type == Camera.CameraTypes.FTP_CAMERA:
                return True
        return False

"""Module containing class to handle WADAS operation modes."""

import logging
import threading
import time
from abc import abstractmethod
from enum import Enum

from PySide6.QtCore import QObject, Signal

from wadas.domain.actuator import Actuator
from wadas.domain.ai_model import AiModel
from wadas.domain.camera import Camera, cameras
from wadas.domain.detection_event import DetectionEvent
from wadas.domain.fastapi_actuator_server import (
    FastAPIActuatorServer,
    initialize_fastapi_logger,
)
from wadas.domain.ftps_server import FTPsServer
from wadas.domain.notifier import Notifier

logger = logging.getLogger(__name__)


class OperationMode(QObject):
    """Class to handle WADAS operation modes."""

    class OperationModeTypes(Enum):
        TestModelMode = "Test Model Mode"
        AnimalDetectionMode = "Animal Detection Mode"
        AnimalDetectionAndClassificationMode = "Animal Detection and Classification Mode"
        TunnelMode = "Tunnel Mode"
        BearDetectionMode = "Bear Detection Mode"
        CustomSpeciesClassificationMode = "Custom Species Classification Mode"

    # Currently selected operation mode
    cur_operation_mode = None
    cur_operation_mode_type = None  # We need this separately as object is deleted after op_mode run
    cur_custom_classification_species = None

    # Signals
    update_image = Signal(str)
    update_actuator_status = Signal()
    update_info = Signal()
    run_finished = Signal()
    run_progress = Signal(int)

    flag_stop_update_actuators_thread = False

    def __init__(self):
        super(OperationMode, self).__init__()
        self.type = None
        self.ai_model = None
        self.last_detection = ""
        self.last_classification = ""
        self.last_classified_animals_str = ""
        self.url = ""
        self.camera_thread = []
        self.ftp_thread = None
        self.actuators_server_thread = None
        self.actuators_view_thread = None

    def init_model(self):
        """Method to run the selected WADAS operation mode"""

        if self.ai_model is None:
            logger.info("initializing model...")
            self.ai_model = AiModel()
        else:
            logger.debug("Model already initialized, skipping initialization.")

    def _initialize_cameras(self):
        """Method to initialize and run the FTP Server
        and threads associated to the cameras (both ftp and usb)"""
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
        """Method to run the animal detection process on a specific image"""
        results, detected_img_path = self.ai_model.process_image(cur_image_path, True)
        self.last_detection = detected_img_path
        return results, detected_img_path

    def _format_classified_animals_string(self, classified_animals):
        # Prepare a list of classified animals to print in UI
        self.last_classified_animals_str = ", ".join(
            animal["classification"][0] for animal in classified_animals
        )

    def _classify(self, cur_image_path, detection_results):
        """Method to run the animal classification process
        on a specific image starting from the detection output"""
        # Classify if detection has identified animals
        if len(detection_results["detections"].xyxy):
            logger.info("Running classification on detection result(s)...")
            (
                classified_img_path,
                classified_animals,
            ) = self.ai_model.classify(cur_image_path, detection_results)
            self.last_classification = classified_img_path

            self._format_classified_animals_string(classified_animals)
            return classified_img_path, classified_animals
        return None, None

    def ftp_camera_exist(self):
        for camera in cameras:
            if camera.type == Camera.CameraTypes.FTP_CAMERA:
                return True
        return False

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

    def _initialize_processes(self):
        """Method to initialize the processes needed for the dectection"""
        self.init_model()
        self.check_for_termination_requests()
        self._initialize_cameras()
        self.start_actuator_server()

    def send_notification(self, detection_event: DetectionEvent, message):
        """Method to send notification(s) trough Notifier class (and subclasses)"""
        Notifier.send_notifications(detection_event, message)

    def actuate(self, camera_id):
        """Method to trigger actuators associated to the camera, when enabled"""
        cur_camera = None
        for cur_camera in cameras:
            if cur_camera.id == camera_id:
                break
        if cur_camera:
            for actuator in cur_camera.actuators:
                if actuator.enabled:
                    actuator.actuate()

    def execution_completed(self):
        """Method to perform end of execution steps."""
        self.run_finished.emit()
        self.stop_ftp_server()
        logger.info("Done with processing.")

    def stop_ftp_server(self):
        """Method to stop FTP server thread"""

        if self.ftp_thread and FTPsServer.ftps_server:
            FTPsServer.ftps_server.server.close_all()
            FTPsServer.ftps_server.server.close()
            self.ftp_thread.join()

    def _scheduled_update_actuators_trigger(self):
        """Method to trigger the actuator(s) view update every 5 secs"""
        while not self.flag_stop_update_actuators_thread:
            time.sleep(5)
            self.update_actuator_status.emit()

    def start_actuator_server(self):
        """Method to start the HTTPS Actuator Server"""
        if Actuator.actuators and FastAPIActuatorServer.actuator_server:
            initialize_fastapi_logger()
            logger.info("Instantiating HTTPS Actuator server...")
            self.actuators_server_thread = FastAPIActuatorServer.actuator_server.run()
            self.actuators_view_thread = self.start_update_actuators_thread()
        else:
            logger.info("No actuator or actuator server defined")

    def start_update_actuators_thread(self):
        """Start the thread responsible for keeping the actuator(s) view updated"""
        update_thread = threading.Thread(target=self._scheduled_update_actuators_trigger)
        if update_thread:
            update_thread.start()
            logger.info("Starting thread for update actuators view...")
        else:
            logger.error("Unable to create new thread for update actuators view.")
        return update_thread

    def stop_update_actuators_thread(self):
        """Method to stop the thread responsible for keeping the actuator(s) view updated"""
        self.flag_stop_update_actuators_thread = True
        if self.actuators_view_thread:
            self.actuators_view_thread.join()

    def stop_actuator_server(self):
        """Method to Stop HTTPS Actuator Server"""
        if FastAPIActuatorServer.actuator_server:
            self.stop_update_actuators_thread()
            FastAPIActuatorServer.actuator_server.stop()
            if self.actuators_server_thread:
                self.actuators_server_thread.join()

    @abstractmethod
    def run(self):
        """Method to run the specific operation mode."""

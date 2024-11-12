"""Module containing class to handle WADAS operation modes."""

import logging
import threading
import time
from enum import Enum

from PySide6.QtCore import QObject, Signal

from wadas.domain.actuator import Actuator
from wadas.domain.ai_model import AiModel
from wadas.domain.camera import cameras
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

    # Currently selected operation mode
    cur_operation_mode = None
    cur_operation_mode_type = None  # We need this separately as object is deleted after op_mode run

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
        self.last_classified_animals = ""
        self.url = ""
        self.email_configuration = {}
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

    def send_notification(self, img_path, message):
        """Method to send notification(s) trough Notifier class (and subclasses)"""
        Notifier.send_notification(img_path, message)

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

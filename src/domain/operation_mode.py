"""Module containing class to handle WADAS operation modes."""

import logging
import threading
import time
from enum import Enum

from PySide6.QtCore import QObject, Signal

from domain.ai_model import AiModel
from domain.feeder_actuator import FeederActuator
from domain.ftps_server import FTPsServer
from domain.notifier import Notifier
from domain.roadsign_actuator import RoadSignActuator

logger = logging.getLogger(__name__)


class OperationMode(QObject):
    """Class to handle WADAS operation modes."""

    class OperationModeTypes(Enum):
        TestModelMode = "Test Model Mode"
        AnimalDetectionMode = "Animal Detection Mode"
        AnimalDetectionAndClassificationMode = "Animal Detection and Classification Mode"
        TunnelMode = "Tunnel Mode"
        BearDetectionMode = "Bear Detection Mode"

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

    def actuate(self, actuator_list):
        """Method to trigger actuators when enabled"""
        # TODO @stefano
        for actuator in actuator_list:
            if actuator.enabled:
                if isinstance(actuator, RoadSignActuator):
                    actuator.send_command(RoadSignActuator.Commands.DISPLAY_ON)
                elif isinstance(actuator, FeederActuator):
                    actuator.send_command(FeederActuator.Commands.OPEN)
                else:
                    raise Exception("Unknown actuator type")

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
        while not self.flag_stop_update_actuators_thread:
            time.sleep(3)
            self.update_actuator_status.emit()

    def start_update_actuators_thread(self):
        update_actuators_thread = threading.Thread(target=self._scheduled_update_actuators_trigger)
        if update_actuators_thread:
            update_actuators_thread.start()
            logger.info("Starting thread for update actuators view...")
        else:
            logger.error("Unable to create new thread for update actuators view.")
        return update_actuators_thread

    def stop_update_actuators_thread(self):
        self.flag_stop_update_actuators_thread = True

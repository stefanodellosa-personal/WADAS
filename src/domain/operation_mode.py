"""Module containing class to handle WADAS operation modes."""

import logging

from enum import Enum

from PySide6.QtCore import QObject, Signal

from domain.actuator import actuators
from domain.ai_model import AiModel
from domain.ftps_server import FTPsServer
from domain.notifier import Notifier

logger = logging.getLogger(__name__)


class OperationMode(QObject):
    """Class to handle WADAS operation modes."""

    class OperationModeTypes(Enum):
        TestModelMode = "Test Model Mode"
        AnimalDetectionMode = "Animal Detection Mode"
        AnimalDetectionAndClassificationMode = (
            "Animal Detection and Classification Mode"
        )
        TunnelMode = "Tunnel Mode"
        BearDetectionMode = "Bear Detection Mode"

    # Signals
    update_image = Signal(str)
    update_info = Signal()
    run_finished = Signal()
    run_progress = Signal(int)

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

    def actuate(self):
        """Method to trigger actuators when enabled"""
        if actuators:
            # TODO: implement actuator logic
            pass

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

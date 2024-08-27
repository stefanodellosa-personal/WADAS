"""Module containing class to handle WADAS operation modes."""

import logging
from PySide6.QtCore import QObject, Signal
from domain.AiModel import AiModel

logger = logging.getLogger(__name__)

class OperationMode(QObject):
    """Class to handle WADAS operation modes."""

    operation_modes = {"test_model_mode", "tunnel_mode", "bear_detection_mode"}
    # Signals
    update_image = Signal(str)
    run_finished = Signal()
    run_progress = Signal(int)

    def __init__(self):
        super(OperationMode, self).__init__()
        self.modename = ""
        self.ai_model = None
        self.last_detection = ""
        self.last_classification = ""
        self.last_classified_animals = ""
        self.url = ""

    def init_model(self):
            """Method to run the selected WADAS operation mode"""
            
            if self.ai_model is None:
                logger.info("initializing model...")
                self.ai_model = AiModel()
            else:
                logger.debug("Model already initialized, skipping initialization.")

"""Module containing class to handle WADAS operation modes."""

import logging
from PySide6.QtCore import QObject, Signal
from domain.AiModel import AiModel

logger = logging.getLogger(__name__)

class OperationMode(QObject):
    """Class to handle WADAS operation modes."""

    operation_modes = {"test_model", "tunnel_mode", "bear_detection_mode"}
    # Signals
    update_image = Signal(str)
    run_finished = Signal()
    run_progress = Signal(int)

    def __init__(self):
        super(OperationMode, self).__init__()
        self.mode = None
        self.last_detection = ""
        self.last_classification = ""
        self.last_classified_animals = []

    def set_mode(self, mode):
        """Method to specfy selected WADAS operation mode"""

        if mode not in OperationMode.operation_modes:
            logger.error("Invalid selected mode %s. Rolling back to test mode.", mode)
            self.mode = "test_model"
        else:
            logger.info("Selected mode: %s", mode)
            self.mode = mode

    def run(self):
        """Method to run the selected WADAS operation mode"""
        
        logger.info("initializing model...")
        self.detector = AiModel()
        self.run_progress.emit(10)

        if self.mode == "test_model":
            self.test_model_mode()
        else:
            #TODO: fillup with other supported modes
            logger.error("Unsupported mode. Run aborted.")
        
        self.run_finished.emit()

    def test_model_mode(self):
        """WADAS test model operation mode"""

        # Select image to run test on...
        url = "https://www.parks.it/tmpFoto/30079_4_PNALM.jpeg"
        # Run detection model
        det_data = self.detector.process_image_from_url(url, "test_model_from_url")
        img_path = det_data[0]
        det_results = det_data[1]
        self.last_detection = img_path
        
        # Trigger image update in WADAS mainwindow
        self.update_image.emit(img_path)

        logger.info("Runnin classification on detection result(s)...")
        img_path = self.detector.classify(img_path, det_results)
        self.last_classification = img_path

        # Trigger image update in WADAS mainwindow
        self.update_image.emit(img_path)

        logger.info("Done with processing.")
from domain.AiModel import ImgDetector
from PySide6.QtCore import QObject, Signal
import logging

logger = logging.getLogger(__name__)

class OperationMode(QObject):
    operation_modes = {"test_model", "tunnel_mode", "bear_detection_mode"}
    # Signals
    update_image = Signal(str)
    run_finished = Signal()
    run_progress = Signal(int)

    def __init__(self):
        super(OperationMode, self).__init__()

    """Method to specfy selected WADAS operation mode"""
    def set_mode(self, mode):
        if mode not in OperationMode.operation_modes:
            logger.error("Invalid selected mode %s. Rolling back to test mode.", mode)
            self.mode = "test_model"
        else:
            logger.info("Selected mode: %s", mode)
            self.mode = mode

    """Method to run the selected WADAS operation mode"""
    def run(self):
        # Initialize detection model
        logger.info("initializing model...")
        self.detector = ImgDetector()
        self.run_progress.emit(10)

        if self.mode == "test_model":
            self.test_model_mode()
        else:
            #TODO: fillup with other supported modes
            logger.info("Unsupported mode. Run aborted.")
        
        self.run_finished.emit()

    """WADAS test model operation mode"""
    def test_model_mode(self):
        url = "https://www.parks.it/tmpFoto/30079_4_PNALM.jpeg"
        img_path = self.detector.process_image_from_url(url, "test_model_from_url")
        # Trigger image update in WADAS mainwindow
        self.update_image.emit(img_path)
        logger.info("Done with processing.")
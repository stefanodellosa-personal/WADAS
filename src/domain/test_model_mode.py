
from domain.operation_mode import OperationMode
from domain.AiModel import AiModel
import logging

logger = logging.getLogger(__name__)

class TestModelMode(OperationMode):
    def __init__(self):
        super(TestModelMode, self).__init__()
        self.modename = "test_model_mode"
        self.url = ""

    def run(self):
            """WADAS test model operation mode"""

            if not self.url:
                logger.error("Invalid URL. Aborting.")
                return

            # Initialize ai model
            self.init_model()

            self.run_progress.emit(10)
            # Run detection model
            det_data = self.ai_model.process_image_from_url(self.url, "test_model_from_url")
            img_path = det_data[0]
            det_results = det_data[1]
            self.last_detection = img_path
            
            # Trigger image update in WADAS mainwindow
            self.update_image.emit(img_path)

            # Classify if detection has identified animals
            if len(det_results["detections"].xyxy) > 0:
                logger.info("Runnin classification on detection result(s)...")
                img_path = self.ai_model.classify(img_path, det_results)
                self.last_classification = img_path

                # Trigger image update in WADAS mainwindow
                self.update_image.emit(img_path)
            else:
                logger.debug("No results to classify.")

            self.run_finished.emit()
            logger.info("Done with processing.")
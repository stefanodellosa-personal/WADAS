# This file is part of WADAS project.
#
# WADAS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WADAS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WADAS. If not, see <https://www.gnu.org/licenses/>.
#
# Author(s): Stefano Dell'Osa, Alessandro Palla, Cesare Di Mauro, Antonio Farina
# Date: 2024-08-16
# Description: Module containing MainWindow class and methods.

import logging
import os

import requests
from PIL import Image

from wadas.domain.detection_event import DetectionEvent
from wadas.domain.operation_mode import OperationMode
from wadas.domain.utils import get_timestamp

logger = logging.getLogger(__name__)


class TestModelMode(OperationMode):
    def __init__(self):
        super(TestModelMode, self).__init__()
        self.modename = "test_model_mode"
        self.url = ""
        self.file_path = ""
        self.last_classified_animals_str = ""
        self.type = OperationMode.OperationModeTypes.TestModelMode

    def _get_image_from_url(self, url):
        """Method to get image from url"""

        logger.info("Processing image from url: %s", url)
        # Opening the image from url
        img = Image.open(requests.get(url, stream=True).raw).convert("RGB")

        # Save image to disk
        os.makedirs("url_imgs", exist_ok=True)
        img_path = os.path.join("url_imgs", "image_test_model_" + str(get_timestamp()) + ".jpg")
        img.save(img_path)
        logger.info("Saved processed image at: %s", img_path)

        return img_path

    def _get_video_from_url(self):
        """Method to get video from url"""

        # TODO: fill up logic
        pass

    def run(self):
        """WADAS test model operation mode"""

        if not self.url and not self.file_path:
            logger.error("Missing required input. Aborting test model mode.")
            self.execution_completed()
            return

        # Initialize ai model
        self.init_model()

        self.check_for_termination_requests()
        self.run_progress.emit(10)

        # Run detection model
        if self.url:
            img_path = self._get_image_from_url(self.url)
            det_results, detected_img_path = self.ai_model.process_image(img_path, True)
            self.last_detection = detected_img_path
        else:
            # Local file based detection TODO: fill up logic
            pass

        # Check if detection has returned results
        if not detected_img_path or not det_results:
            self.execution_completed()
            return

        # Since we don't have cameras in Test Model Mode,
        # we create dummy detection event with VirtualTestCamera
        detection_event = DetectionEvent(
            "VirtualTestCamera", get_timestamp(), img_path, detected_img_path, det_results, True
        )
        # Trigger image update in WADAS mainwindow
        self.update_image.emit(detection_event.detection_img_path)
        message = "WADAS has detected an animal!"
        self.check_for_termination_requests()

        # Classify if detection has identified animals
        if len(detection_event.detected_animals["detections"].xyxy):
            logger.info("Running classification on detection result(s)...")

            self._classify(detection_event)
            if detection_event.classification_img_path:
                # Trigger image update in WADAS mainwindow
                self.update_image.emit(detection_event.classification_img_path)
                self.update_info.emit()
                message = (
                    f"WADAS has classified '{self.last_classified_animals_str}' "
                    f"animal from camera {detection_event.classification_img_path}!"
                )
            else:
                logger.info("No animal classified.")
                message = ""

        # Send notification
        self.send_notification(detection_event, message)
        self.execution_completed()

    def check_for_termination_requests(self):
        """Terminate current thread if interrupt request comes from Mainwindow."""

        if self.thread().isInterruptionRequested():
            self.run_finished.emit()
            logger.info("Request to stop received. Aborting...")
            return

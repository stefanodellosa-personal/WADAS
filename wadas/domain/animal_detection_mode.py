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
# Date: 2024-09-12
# Description: Animal Detection and Classification module.

import logging
from queue import Empty

from wadas.domain.camera import media_queue
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

    def run(self):
        """WADAS animal detection and classification mode"""

        self._initialize_processes()
        self.check_for_termination_requests()

        # Run detection model
        while self.process_queue:
            self.check_for_termination_requests()
            # Get media (images or videos) from motion detection notification
            # Timeout is set to 1 second to avoid blocking the thread
            try:
                cur_media = media_queue.get(timeout=1)
            except Empty:
                cur_media = None

            # Media processing
            if cur_media and (
                OperationMode.is_image(cur_media["img"]) or OperationMode.is_video(cur_media["img"])
            ):
                logger.debug("Processing media from motion detection notification...")

                detection_event = self._detect(cur_media, self.en_classification)
                self.check_for_termination_requests()

                if detection_event:
                    if self.en_classification:
                        # Classification is enabled
                        if detection_event.classification_img_path:
                            # Trigger image update in WADAS mainwindow with classification result
                            self.update_image.emit(detection_event.classification_img_path)
                            message = (
                                f"WADAS has classified '{self.last_classified_animals_str}' "
                                f"animal from camera {cur_media['img_id']}!"
                            )
                        else:
                            logger.info("No animal classified.")
                            message = ""
                    else:
                        # Trigger image update in WADAS mainwindow with detection result
                        self.update_image.emit(detection_event.detection_img_path)
                        message = "WADAS has detected an animal from camera %s!" % id
                    self.update_info.emit()

                    # Actuation
                    if detection_event:
                        self.actuate(detection_event)

                    # Notification
                    if message:
                        self.send_notification(detection_event, message)
                else:
                    logger.debug("No animal detected.")

        self.execution_completed()

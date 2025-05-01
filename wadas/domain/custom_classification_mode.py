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
# Date: 2024-12-16
# Description: Custom Classification module.

import logging
from queue import Empty

from wadas.ai.models import txt_animalclasses
from wadas.domain.ai_model import AiModel
from wadas.domain.animal_detection_mode import AnimalDetectionAndClassificationMode
from wadas.domain.camera import media_queue
from wadas.domain.operation_mode import OperationMode

logger = logging.getLogger(__name__)


class CustomClassificationMode(AnimalDetectionAndClassificationMode):
    """Custom Classification Mode class."""

    def __init__(self, custom_target_species=None):
        super().__init__()
        self.process_queue = True
        self.type = OperationMode.OperationModeTypes.CustomSpeciesClassificationMode
        self.custom_target_species = custom_target_species

    def set_animal_species(self, target_animal_label):
        """Method to select animal to classify according to Ai model availability"""
        if target_animal_label in txt_animalclasses[AiModel.language]:
            self.custom_target_species = target_animal_label
            logger.debug("%s species selected.", target_animal_label)
            return True
        else:
            logger.error("The specified animal species is not handled by WADAS")
            return False

    def run(self):
        """WADAS custom classification mode"""

        self._initialize_processes()
        self.check_for_termination_requests()

        # Run detection model
        while self.process_queue:
            self.check_for_termination_requests()
            # Get image from motion detection notification
            # Timeout is set to 1 second to avoid blocking the thread
            try:
                cur_img = media_queue.get(timeout=1)
            except Empty:
                cur_img = None

            if cur_img:
                logger.debug("Processing image from motion detection notification...")
                detection_event = self._detect(cur_img)

                self.check_for_termination_requests()
                if detection_event and self.enable_classification:
                    if detection_event.classification_img_path:
                        # Send notification and trigger actuators if the target animal is found
                        if any(
                            classified_animal["classification"][0] == self.custom_target_species
                            for classified_animal in detection_event.classified_animals
                        ):
                            # Notification
                            message = (
                                f"WADAS has classified '{self.last_classified_animals_str}' "
                                f"animal from camera {detection_event.camera_id}!"
                            )
                            logger.info(message)
                            self.send_notification(detection_event, message)

                            # Actuation
                            self.actuate(detection_event)
                        else:
                            logger.info(
                                "Target animal '%s' not found, found '%s' instead. "
                                "Skipping notification.",
                                self.custom_target_species,
                                self.last_classified_animals_str,
                            )

                        # Show processing results in UI
                        self._show_processed_results(detection_event)
                    else:
                        logger.info("No animal classified.")

        self.execution_completed()

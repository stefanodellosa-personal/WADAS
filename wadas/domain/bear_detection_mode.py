"""Bear Detection mode module."""

import logging

from wadas.domain.custom_classification_mode import CustomClassificationMode
from wadas.domain.operation_mode import OperationMode

logger = logging.getLogger(__name__)


class BearDetectionMode(CustomClassificationMode):
    """Bear Detection Mode class."""

    def __init__(self):
        super().__init__("bear")
        self.type = OperationMode.OperationModeTypes.BearDetectionMode

    def serialize(self):
        """Method to serialize Bear Detection Mode object into file."""

        return {"type": self.type.value, "custom_target_species": self.custom_target_species}

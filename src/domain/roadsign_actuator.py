import json
import logging
from enum import Enum

from domain.actuator import Actuator

logger = logging.getLogger(__name__)


class RoadSignActuator(Actuator):
    """RoadSignActuator, specialization of Actuator."""

    class Commands(Enum):
        DISPLAY_ON = json.dumps({"display": True})

    def __init__(self, id, enabled):
        super().__init__(id, enabled)
        self.type = Actuator.ActuatorTypes.ROADSIGN

    def send_command(self, cmd):
        """Method to send the specific command to the Actuator superclass."""
        if isinstance(cmd, RoadSignActuator.Commands):
            super().send_command(cmd)
        else:
            logger.error(
                "Actuator %s with ID %s received an unknown command: %s.",
                self.type,
                self.id,
                cmd,
            )
            raise Exception("Unknown command.")

    def serialize(self):
        """Method to serialize RoadSignActuator object into file."""
        return {"id": self.id, "enabled": self.enabled, "type": self.type.value}

    @staticmethod
    def deserialize(data):
        """Method to deserialize Actuator object from file."""
        return RoadSignActuator(data["id"], data["enabled"])

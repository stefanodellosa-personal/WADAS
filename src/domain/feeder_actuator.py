import json
import logging
from enum import Enum

from domain.actuator import Actuator

logger = logging.getLogger(__name__)


class FeederActuator(Actuator):
    """FeederActuator, specialization of Actuator."""

    class Commands(Enum):
        OPEN = json.dumps({"open": True})

    def __init__(self, id, enabled):
        super().__init__(id, enabled)
        self.type = Actuator.ActuatorTypes.FEEDER

    def send_command(self, cmd):
        """Method to send the specific command to the Actuator superclass."""
        if isinstance(cmd, FeederActuator.Commands):
            super().send_command(cmd)
        else:
            logger.error(
                "Actuator %s with ID %s received an unknown command: %s.",
                self.type,
                self.id,
                cmd,
            )
            raise Exception("Unknown command")

    def serialize(self):
        """Method to serialize Actuator object into file."""
        return {
            "id": self.id,
            "enabled": self.enabled,
        }

    @staticmethod
    def deserialize(data):
        """Method to deserialize Actuator object from file."""
        return FeederActuator(data["id"], data["enabled"])

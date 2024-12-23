import json
import logging
from enum import Enum

from wadas.domain.actuator import Actuator

logger = logging.getLogger(__name__)


class FeederActuator(Actuator):
    """FeederActuator, specialization of Actuator."""

    class Commands(Enum):
        OPEN = json.dumps({"open": True})
        CLOSE = json.dumps({"close": True})

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

    def actuate(self):
        """Method to trigger the FeederActuator sending it the CLOSE Command"""
        self.send_command(self.Commands.CLOSE)

    def serialize(self):
        """Method to serialize Actuator object into file."""
        return {"id": self.id, "enabled": self.enabled, "type": self.type.value}

    @staticmethod
    def deserialize(data):
        """Method to deserialize Actuator object from file."""
        return FeederActuator(data["id"], data["enabled"])

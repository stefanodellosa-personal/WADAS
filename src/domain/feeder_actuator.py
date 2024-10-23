from enum import Enum
import json
import logging

from domain.actuator import Actuator

logger = logging.getLogger(__name__)


class FeederActuator(Actuator):
    """FeederActuator, specialization of Actuator."""

    class Commands(Enum):
        OPEN = json.dumps({"open": True})

    def send_command(self, cmd):
        """Method to send the specific command to the Actuator superclass."""
        if isinstance(cmd, FeederActuator.Commands):
            super().send_command(cmd)
        else:
            logger.error("Actuator %s with ID %s received an unknown command: %s.", self.__class__.__name__,
                         self.actuator_id, cmd)
            raise Exception("Unknown command")

    def serialize(self):
        """Method to serialize Actuator object into file."""
        return {
            "type": self.__class__.__name__,
            "id": self.actuator_id,
            "enabled": self.enabled,
        }

    @staticmethod
    def deserialize(data):
        """Method to deserialize Actuator object from file."""
        return FeederActuator(**data)

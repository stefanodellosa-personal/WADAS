from enum import Enum
import json

from domain.actuator import Actuator


class FeederActuator(Actuator):
    """FeederActuator, specialization of Actuator."""

    class Commands(Enum):
        open = json.dumps({'open': True})

    def send_command(self, msg):
        if isinstance(msg, FeederActuator.Commands):
            super().send_command(msg)
        else:
            raise Exception("Unknown command")

    def serialize(self):
        """Method to serialize Actuator object into file."""
        return {
            "type": self.__class__.__name__,
            "id": self.actuator_id,
            "enabled": self.enabled
        }

    @staticmethod
    def deserialize(data):
        """Method to deserialize Actuator object from file."""
        return FeederActuator(**data)

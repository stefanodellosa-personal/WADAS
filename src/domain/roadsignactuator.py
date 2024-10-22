from enum import Enum
import json

from domain.actuator import Actuator


class RoadSignActuator(Actuator):
    """RoadSignActuator, specialization of Actuator."""

    class Commands(Enum):
        display_on = json.dumps({"display": True})

    def send_command(self, msg):
        if isinstance(msg, RoadSignActuator.Commands):
            super().send_command(msg)
        else:
            raise Exception("Unknown command")

    def serialize(self):
        """Method to serialize RoadSignActuator object into file."""
        return {
            "type": self.__class__.__name__,
            "id": self.actuator_id,
            "enabled": self.enabled,
        }

    @staticmethod
    def deserialize(data):
        """Method to deserialize Actuator object from file."""
        return RoadSignActuator(**data)

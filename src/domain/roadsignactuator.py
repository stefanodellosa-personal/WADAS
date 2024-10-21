import json
from enum import Enum

from domain.actuator import Actuator


class RoadSignActuator(Actuator):
    """RoadSignActuator, specialization of Actuator."""

    class Commands(Enum):
        DisplayON = json.dumps({'display': True})

    def __init__(self, id, enabled=False):
        super().__init__(id, enabled=enabled)
        self.type = Actuator.ActuatorTypes.RoadSignActuator

    def send_command(self, msg):
        if isinstance(msg, RoadSignActuator.Commands):
            super().send_command(msg)
        else:
            raise Exception("Command not supported")

    def serialize(self):
        """Method to serialize RoadSignActuator object into file."""
        return dict(
            type=self.type.value,
            id=self.id,
            enabled=self.enabled
        )

    @staticmethod
    def deserialize(data):
        """Method to deserialize Actuator object from file."""
        return RoadSignActuator(data["id"], enabled=data["enabled"])

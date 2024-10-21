import json
from enum import Enum

from domain.actuator import Actuator


class FeederActuator(Actuator):
    """FeederActuator, specialization of Actuator."""

    class Commands(Enum):
        Open = json.dumps({'open': True})

    def __init__(self, id, enabled=False):
        super().__init__(id, enabled=enabled)
        self.type = Actuator.ActuatorTypes.FeederActuator

    def send_command(self, msg):
        if isinstance(msg, FeederActuator.Commands):
            super().send_command(msg)
        else:
            raise Exception("Command not supported")

    def serialize(self):
        """Method to serialize Actuator object into file."""
        return dict(
            type=self.type.value,
            id=self.id,
            enabled=self.enabled
        )

    @staticmethod
    def deserialize(data):
        """Method to deserialize Actuator object from file."""
        return FeederActuator(data["id"], enabled=data["enabled"])

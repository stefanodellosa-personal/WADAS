"""Actuator module"""

import datetime
import json
import logging
from abc import abstractmethod
from enum import Enum
from queue import Queue, Empty

logger = logging.getLogger(__name__)


class Actuator:
    """Base class of an actuator."""

    actuators_pool = {}

    class ActuatorTypes(Enum):
        RoadSignActuator = "RoadSignActuator"
        FeederActuator = "FeederActuator"

    def __init__(self, id, enabled=False):
        self.type = None
        self.cmd_queue = Queue()
        self.id = id
        self.last_update = None
        self.enabled = enabled
        self.stop_thread = False
        Actuator.actuators_pool[self.id] = self

    def send_command(self, msg: Enum):
        self.cmd_queue.put(msg.value)

    def get_command(self):
        self.last_update = datetime.datetime.now()
        try:
            return self.cmd_queue.get(block=False)
        except Empty:
            return None

    @abstractmethod
    def serialize(self):
        """Method to serialize Actuator object into file."""
        pass

    @staticmethod
    def deserialize(data):
        """Method to deserialize Actuator object from file."""
        pass


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

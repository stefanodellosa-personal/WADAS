"""Actuator module"""

import datetime
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

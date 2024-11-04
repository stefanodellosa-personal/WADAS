"""Actuator module"""

import datetime
import logging
from abc import abstractmethod
from enum import Enum
from queue import Empty, Queue

logger = logging.getLogger(__name__)


class Actuator:
    """Base class of an actuator."""

    actuators = {}

    class ActuatorTypes(Enum):
        ROADSIGN = "Road Sign"
        FEEDER = "Feeder"

    def __init__(self, actuator_id, enabled=False):
        self.cmd_queue = Queue()
        self.id = actuator_id
        self.last_update = None
        self.enabled = enabled
        self.stop_thread = False
        self.type = None

    def send_command(self, cmd: Enum):
        """Method to insert a command into the actuator queue"""
        self.cmd_queue.put(cmd.value)

    def get_command(self):
        """Method to get the last command of the queue"""
        self.last_update = datetime.datetime.now()
        try:
            return self.cmd_queue.get(block=False)
        except Empty:
            return None  # if there are no commands, return None

    @abstractmethod
    def actuate(self):
        """Method to trigger the actuator sending the appropriate command"""
        pass

    @abstractmethod
    def serialize(self):
        """Method to serialize Actuator object into file."""
        pass

    @staticmethod
    def deserialize(data):
        """Method to deserialize Actuator object from file."""
        pass

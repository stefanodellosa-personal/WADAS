"""Actuator module"""

from abc import abstractmethod
import datetime
from enum import Enum
import logging
from queue import Empty, Queue

logger = logging.getLogger(__name__)


class Actuator:
    """Base class of an actuator."""

    actuators = {}

    def __init__(self, actuator_id, enabled=False):
        self.cmd_queue = Queue()
        self.actuator_id = actuator_id
        self.last_update = None
        self.enabled = enabled
        self.stop_thread = False
        Actuator.actuators[self.actuator_id] = self

    def send_command(self, cmd: Enum):
        """Method to insert a command into the actuator queue"""
        self.cmd_queue.put(cmd.value)

    def get_command(self):
        """Method to get the last command of the queue"""
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

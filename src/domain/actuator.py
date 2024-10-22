"""Actuator module"""

from abc import abstractmethod
import datetime
from enum import Enum
import logging
from queue import Empty, Queue

logger = logging.getLogger(__name__)


class Actuator:
    """Base class of an actuator."""

    actuators_pool = {}

    def __init__(self, actuator_id, enabled=False):
        self.cmd_queue = Queue()
        self.actuator_id = actuator_id
        self.last_update = None
        self.enabled = enabled
        self.stop_thread = False
        Actuator.actuators_pool[self.actuator_id] = self

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

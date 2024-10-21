"""Actuator module"""

import logging
from abc import abstractmethod
from enum import Enum

logger = logging.getLogger(__name__)

# List of Actuators
actuators = []


class Actuator:
    """Base class of an actuator."""

    class ActuatorTypes(Enum):
        Semaphore = "Semaphore"
        Feeder = "Feeder"

    def __init__(self, id, enabled=False):
        self.type = None
        self.id = id
        self.enabled = enabled
        self.stop_thread = False

    @abstractmethod
    def serialize(self):
        """Method to serialize Actuator object into file."""
        pass

    @staticmethod
    def deserialize(data):
        """Method to deserialize Actuator object from file."""
        pass

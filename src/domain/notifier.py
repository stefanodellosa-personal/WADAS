"""Notification module"""

import logging
from abc import abstractmethod
from enum import Enum
from queue import Queue

logger = logging.getLogger(__name__)

# List of notifiers
notifiers = []


class Notifier:
    """Base class for notifiers."""

    class NotifierTypes(Enum):
        Email = "Email"

    def __init__(self, enabled=True):
        self.type = None
        self.enabled = enabled

    @abstractmethod
    def serialize(self):
        """Method to serialize Camera object into file."""
        pass

    @staticmethod
    def deserialize(data):
        """Method to deserialize Camera object from file."""
        pass

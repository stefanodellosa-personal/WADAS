"""Notification module"""

import logging
from abc import abstractmethod
from enum import Enum

logger = logging.getLogger(__name__)


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


# List of notifiers
notifiers = dict.fromkeys([Notifier.NotifierTypes.Email.value])

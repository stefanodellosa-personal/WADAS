"""Notification module"""

import logging
from abc import abstractmethod
from enum import Enum

logger = logging.getLogger(__name__)


class Notifier:
    """Base class for notifiers."""

    class NotifierTypes(Enum):
        EMAIL = "Email"
        WHATSAPP = "WhatsApp"

    notifiers = dict.fromkeys([NotifierTypes.EMAIL.value, NotifierTypes.WHATSAPP.value])

    def __init__(self, enabled=True, allow_images=True):
        self.type = None
        self.enabled = enabled
        self.allow_images = allow_images

    @staticmethod
    def send_notifications(img_path, message=""):
        """Method to send notification through enabled protocols."""

        configured_notifier = False
        enabled_notifier = False
        for notifier in Notifier.notifiers:
            if Notifier.notifiers[notifier]:
                if Notifier.notifiers[notifier].is_configured:
                    configured_notifier = True
                    if Notifier.notifiers[notifier].enabled:
                        enabled_notifier = True
                        Notifier.notifiers[notifier].send_notification(img_path)
        if not configured_notifier:
            logger.warning("No notification protocol configured. Skipping notification.")
        elif not enabled_notifier:
            logger.warning("No notification protocol enabled. Skipping notification.")

    @abstractmethod
    def is_configured(self):
        """Method to return whether a given Notifier is properly configured"""

    @abstractmethod
    def send_notification(self, img_path):
        """Method to send notification for specific Notifier."""

    @abstractmethod
    def serialize(self):
        """Method to serialize Camera object into file."""

    @staticmethod
    def deserialize(data):
        """Method to deserialize Camera object from file."""

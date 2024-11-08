"""Notification module"""

import logging
from abc import abstractmethod
from enum import Enum

import keyring

logger = logging.getLogger(__name__)


class Notifier:
    """Base class for notifiers."""

    class NotifierTypes(Enum):
        EMAIL = "Email"

    notifiers = dict.fromkeys([NotifierTypes.EMAIL.value])

    def __init__(self, enabled=True):
        self.type = None
        self.enabled = enabled

    @staticmethod
    def send_notification(img_path, message=""):
        """Method to send notification through enabled protocols."""

        configured_notifier = False
        enabled_notifier = False
        for notifier in Notifier.notifiers:
            if Notifier.notifiers[notifier]:
                if Notifier.notifiers[notifier].type == Notifier.NotifierTypes.EMAIL:
                    username = Notifier.notifiers[notifier].sender_email
                    credentials = keyring.get_credential("WADAS_email", username)
                    if (
                        Notifier.notifiers[notifier].smtp_hostname
                        and Notifier.notifiers[notifier].smtp_port
                        and Notifier.notifiers[notifier].recipients_email
                        and credentials.username
                    ):
                        configured_notifier = True
                        if Notifier.notifiers[notifier].enabled:
                            enabled_notifier = True
                            Notifier.notifiers[notifier].send_email(img_path)
                # add here other notification protocols.
        if not configured_notifier:
            logger.warning("No notification protocol configured. Skipping notification.")
        elif not enabled_notifier:
            logger.warning("No notification protocol enabled. Skipping notification.")

    @abstractmethod
    def serialize(self):
        """Method to serialize Camera object into file."""

    @staticmethod
    def deserialize(data):
        """Method to deserialize Camera object from file."""

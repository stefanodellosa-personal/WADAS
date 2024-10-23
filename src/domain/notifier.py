"""Notification module"""

import logging
from abc import abstractmethod
from enum import Enum

import keyring

logger = logging.getLogger(__name__)


class Notifier:
    """Base class for notifiers."""

    class NotifierTypes(Enum):
        Email = "Email"

    notifiers = dict.fromkeys([NotifierTypes.Email.value])

    def __init__(self, enabled=True):
        self.type = None
        self.enabled = enabled

    @staticmethod
    def send_notification(img_path, message=""):
        """Method to send notification through enabled protocols."""

        sent = False
        for notifier in Notifier.notifiers:
            if Notifier.notifiers[notifier].type == Notifier.NotifierTypes.Email:
                username = Notifier.notifiers[notifier].sender_email
                credentials = keyring.get_credential("WADAS_email", username)
                if (
                    Notifier.notifiers[notifier].smtp_hostname
                    and Notifier.notifiers[notifier].smtp_port
                    and Notifier.notifiers[notifier].recipients_email
                    and credentials.username
                ):
                    sent = Notifier.notifiers[notifier].send_email(img_path)
            # add here other notification protocols.
        if not sent:
            logger.warning("No notification protocol set. Skipping notification.")

    @abstractmethod
    def serialize(self):
        """Method to serialize Camera object into file."""

    @staticmethod
    def deserialize(data):
        """Method to deserialize Camera object from file."""

"""WhatsApp notifier module"""

import logging

import keyring
import requests

from wadas.domain.notifier import Notifier

logger = logging.getLogger(__name__)


class WhatsAppNotifier(Notifier):
    """WhatsApp Notifier Class"""

    def __init__(self, sender_id, recipient_numbers, enabled=True, allow_images=True):
        super().__init__(enabled)
        self.type = Notifier.NotifierTypes.WHATSAPP
        self.sender_id = sender_id
        self.recipient_numbers = recipient_numbers
        self.allow_images = allow_images

    def is_configured(self):
        """Method that returns configuration status as bool value."""

        credentials = keyring.get_credential("WADAS_WhatsApp", self.sender_id)
        return (
            self.sender_id
            and self.recipient_numbers
            and credentials.username
            and credentials.password
        )

    def send_notification(self, img_path):
        """Implementation of send_notification method for WhatsApp notifier."""

    def send_whatsapp_message(self, img_path):
        """Method to send WhatsApp message notification."""

        message = "WADAS: Animal Detected!"
        url = f"https://graph.facebook.com/v17.0/{self.sender_id}/messages"
        access_token = ""  # TODO: fetch it from keyring
        recipient_phone_number = ""  # TODO: fetch it from notifier class

        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

        data = {
            "messaging_product": "whatsapp",
            "to": recipient_phone_number,
            "type": "text",
            "text": {"body": message},
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            logger.info("WhatsApp notification sent!")
        else:
            logger.error(response.status_code, response.text)

    def serialize(self):
        """Method to serialize email notifier object into file."""
        return {
            "sender_id": self.sender_id,
            "recipient_numbers": self.recipient_numbers,
            "enabled": self.enabled,
            "allow_images": self.allow_images,
        }

    @staticmethod
    def deserialize(data):
        """Method to deserialize email notifier object from file."""
        return WhatsAppNotifier(**data)

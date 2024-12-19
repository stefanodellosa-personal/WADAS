"""Telegram notifier module"""

import logging
import os

import requests

from wadas.domain.notifier import Notifier
from wadas.domain.utils import image_to_base64

logger = logging.getLogger(__name__)

module_dir_path = os.path.dirname(os.path.abspath(__file__))


class TelegramNotifier(Notifier):
    """Telegram Notifier Class"""

    BASE_URL = "https://localhost:8443/api/v1/telegram"
    REGISTRATION_URL = BASE_URL + "/users"
    NOTIFICATION_URL = BASE_URL + "/notifications"

    def __init__(self, org_code, recipient_user_ids=None, enabled=True, allow_images=True):
        super().__init__(enabled)

        self.type = Notifier.NotifierTypes.TELEGRAM
        self.org_code = org_code
        self.recipient_user_ids = recipient_user_ids if recipient_user_ids is not None else []
        self.allow_images = allow_images

    def is_configured(self):
        """Method that returns configuration status as bool value."""
        return self.org_code is not None and len(self.recipient_user_ids) > 0

    def register_new_user(self):
        """Method to enable Telegram notification to a new user."""
        if self.org_code:
            data = {"org_code": self.org_code}
            res = requests.post(self.REGISTRATION_URL, json=data, verify=False)
            if res.status_code == 200:
                user_id = res.json()["user_id"]
                self.recipient_user_ids.append(user_id)
                return user_id
            else:
                logger.error(
                    "Unable to retrieve user_id from Telegram backend. Error: %s - %s",
                    str(res.status_code),
                    res.text,
                )
                return None
        else:
            raise Exception("Organization code is not valid")

    def send_notification(self, img_path):
        """Implementation of send_notification method for Telegram notifier."""

        self.send_telegram_message(img_path)

    def send_telegram_message(self, img_path):
        """Method to send Telegram message notification."""

        message = "WADAS: Animal Detected!"

        data = {
            "org_code": self.org_code,
            "user_ids": self.recipient_user_ids,
            "message": message,
            "image_b64": image_to_base64(img_path),
        }

        try:
            res = requests.post(self.NOTIFICATION_URL, json=data, verify=False)
            if res.status_code == 200:
                logger.info("Telegram notifications sent!")
            else:
                logger.error(
                    "Problem sending Telegram notifications: %s - %s",
                    str(res.status_code),
                    res.text,
                )
        except Exception as e:
            logger.error("Problem sending Telegram notifications: %s", str(type(e)))

    def serialize(self):
        """Method to serialize Telegram notifier object into file."""
        return {
            "org_code": self.org_code,
            "recipient_user_ids": self.recipient_user_ids,
            "enabled": self.enabled,
            "allow_images": self.allow_images,
        }

    @staticmethod
    def deserialize(data):
        """Method to deserialize Telegram notifier object from file."""
        return TelegramNotifier(**data)

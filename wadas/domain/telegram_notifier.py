"""Telegram notifier module"""

import logging
import os

import requests

from wadas.domain.notifier import Notifier
from wadas.domain.telegram_recipient import TelegramRecipient
from wadas.domain.utils import image_to_base64

logger = logging.getLogger(__name__)

module_dir_path = os.path.dirname(os.path.abspath(__file__))


class TelegramNotifier(Notifier):
    """Telegram Notifier Class"""

    BASE_URL = "https://wadas.hopto.org:8443/api/v1/telegram"
    REGISTRATION_URL = BASE_URL + "/users"
    NOTIFICATION_URL = BASE_URL + "/notifications"

    def __init__(self, org_code, recipients=None, enabled=True, allow_images=True):
        super().__init__(enabled)

        self.type = Notifier.NotifierTypes.TELEGRAM
        self.org_code = org_code
        self.recipients = recipients if recipients is not None else []
        self.allow_images = allow_images

    def is_configured(self):
        """Method that returns configuration status as bool value."""
        return self.org_code is not None and len(self.recipients) > 0

    def get_recipient_by_id(self, recipient_id):
        if self.recipients is not None:
            for r in self.recipients:
                if r.recipient_id == recipient_id:
                    return r
        return None

    def fetch_registered_recipient(self):
        res = requests.get(f"{self.REGISTRATION_URL}?org_code={self.org_code}", verify=False)
        if res.status_code == 200:
            list_users = res.json()
            updated_receivers = []
            for user_id in list_users:
                known_recipient = self.get_recipient_by_id(user_id)
                if known_recipient:
                    updated_receivers.append(known_recipient)
                else:
                    updated_receivers.append(TelegramRecipient(user_id))

            self.recipients = updated_receivers
        else:
            raise Exception("Impossible to retrieve registered users")

    def register_new_recipient(self):
        """Method to enable Telegram notification to a new user."""
        if self.org_code:
            data = {"org_code": self.org_code}
            res = requests.post(self.REGISTRATION_URL, json=data, verify=False)
            if res.status_code == 200:
                recipient_id = res.json()["user_id"]
                telegram_recipient = TelegramRecipient(recipient_id)
                self.recipients.append(telegram_recipient)
                return telegram_recipient
            else:
                logger.error(
                    "Unable to retrieve user_id from Telegram backend. Error: %s - %s",
                    str(res.status_code),
                    res.text,
                )
                return None
        else:
            raise Exception("Organization code is not valid")

    def remove_registered_recipient(self, recipient):
        res = requests.delete(
            f"{self.REGISTRATION_URL}?org_code={self.org_code}&user_id={recipient.recipient_id}",
            verify=False,
        )
        if res.status_code == 204:
            self.recipients.remove(recipient)
        else:
            raise Exception("Impossible to delete the recipient")

    def send_notification(self, img_path):
        """Implementation of send_notification method for Telegram notifier."""

        self.send_telegram_message(img_path)

    def send_telegram_message(self, message, img_path=None):
        """Method to send Telegram message notification."""

        data = {
            "org_code": self.org_code,
            "user_ids": [recipient.recipient_id for recipient in self.recipients],
            "message": message,
        }

        if img_path:
            data["image_b64"] = image_to_base64(img_path)

        try:
            res = requests.post(self.NOTIFICATION_URL, json=data, verify=False)
            if res.status_code == 200:
                logger.info("Telegram notifications sent!")
                return res.json()
            else:
                logger.error(
                    "Problem sending Telegram notifications: %s - %s",
                    str(res.status_code),
                    res.text,
                )
                raise Exception(
                    f"Problem sending Telegram notifications: {str(res.status_code)} - {res.text}"
                )
        except Exception as e:
            logger.error("Problem sending Telegram notifications: %s", str(type(e)))
            raise

    def serialize(self):
        """Method to serialize Telegram notifier object into file."""
        return {
            "org_code": self.org_code,
            "recipients": [recipient.serialize() for recipient in self.recipients],
            "enabled": self.enabled,
            "allow_images": self.allow_images,
        }

    @staticmethod
    def deserialize(data):
        """Method to deserialize Telegram notifier object from file."""
        new_data = data.copy()
        recipient_list = new_data["recipients"]
        new_data["recipients"] = [
            TelegramRecipient.deserialize(recipient) for recipient in recipient_list
        ]
        return TelegramNotifier(**new_data)

"""Email notifier module"""

from domain.notifier import Notifier


class EmailNotifier(Notifier):
    """Email Notifier Class"""

    def __init__(self, smtp_hostname, smtp_port, recipients_email, enabled=True):
        super().__init__(enabled)
        self.type = Notifier.NotifierTypes.Email
        self.smtp_hostname = smtp_hostname
        self.smtp_port = smtp_port
        self.recipients_email = recipients_email

    def serialize(self):
        """Method to serialize email notifier object into file."""
        return dict(
            type=self.type.value,
            smtp_hostname=self.type.smtp_hostname,
            smtp_port=self.smtp_port,
            recipients_email=self.recipients_email,
        )

    @staticmethod
    def deserialize(data):
        """Method to deserialize email notifier object from file."""
        return EmailNotifier(
            data["type"],
            data["smtp_hostname"],
            data["smtp_port"],
            data["recipients_email"],
        )

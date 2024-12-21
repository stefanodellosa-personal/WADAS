class TelegramRecipient:

    def __init__(self, recipient_id, name=None):
        self.recipient_id = recipient_id
        self.name = name

    def __eq__(self, other):
        if not hasattr(other, "recipient_id"):
            return False
        return self.recipient_id == other.recipient_id

    def serialize(self):
        """Method to serialize TelegramRecipient object into file."""
        return {"recipient_id": self.recipient_id, "name": self.name}

    @staticmethod
    def deserialize(data):
        """Method to deserialize TelegramRecipient object from file."""
        return TelegramRecipient(**data)

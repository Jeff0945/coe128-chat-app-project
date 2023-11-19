from datetime import datetime

from services.collection import Collection


class Message(Collection):
    required = ["sender_id", "recipient_id", "message"]

    id: int = None
    sender_id: int = None
    recipient_id: int | str = None
    message: str = None
    created_at: datetime = None

    def __init__(self, data: dict):
        self.validate(data)

        self.id = self.assign_id()
        self.sender_id = data.get("sender_id")
        self.recipient_id = data.get("recipient_id")
        self.message = data.get("message")
        self.created_at = datetime.now()

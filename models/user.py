from socket import socket
from models.message import Message
from services.collection import Collection
import communication


class User(Collection):
    required = ["name", "connection"]

    id: int = None
    name: str = None
    connection: socket = None

    def __init__(self, data: dict):
        self.validate(data)

        self.id = self.assign_id()
        self.name = data.get("name")
        self.connection = data.get("connection")

    def send_message(self, message):
        communication.send_message(self.connection, message)

    def sent_messages(self, recipient_id: int | None = None):
        sent_messages = Message.where("sender_id", "=", self.id)

        if recipient_id is not None:
            return sent_messages.where("recipient_id", "=", recipient_id).get()
        else:
            return sent_messages.get()

    def received_messages(self, sender_id: int | None = None):
        received_messages = Message.where("recipient_id", "=", self.id)

        if sender_id is not None:
            return received_messages.where("sender_id", "=", sender_id).get()
        else:
            return received_messages.get()

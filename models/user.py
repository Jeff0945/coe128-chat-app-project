from socket import socket
from services.collection import Collection
import communication


class User(Collection):
    id: int = None
    name: str = None
    connection: socket = None

    def __init__(self, name: str, connection: socket):
        self.id = self.assign_id()
        self.name = name
        self.connection = connection

    def send_message(self, message):
        communication.send_message(self.connection, message)

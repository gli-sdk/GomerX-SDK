from .client import Client
from .message import Message


class Module(object):
    def __init__(self, client: Client):
        self._client = client

    @property
    def client(self):
        return self._client

    def send_msg(self, msg: Message):
        self.client.send(msg)

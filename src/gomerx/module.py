from . import protocol

__all__ = ['Module']


class Module(object):
    _client = None
    _robot = None

    def __init__(self, robot):
        self._robot = robot
        self._client = robot.client

    @property
    def client(self):
        return self._client

    def start(self):
        pass

    def stop(self):
        pass

    def _send_sync_proto(self, proto):
        if not self.client:
            return False
        msg = protocol.Message(proto)
        resp_msg = self._client.send_sync_msg(msg)
        return True

    def _send_async_proto(self, proto):
        if not self.client:
            return False
        msg = protocol.Message(proto)
        return self._client.send_sync_msg(msg)

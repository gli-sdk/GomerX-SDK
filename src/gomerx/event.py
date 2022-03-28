import threading
from . import message


class Dispatcher(object):
    _instance_lock = threading.Lock()
    _in_progress_mutex = threading.Lock()
    _in_progress = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(Dispatcher, "_instance"):
            with Dispatcher._instance_lock:
                if not hasattr(Dispatcher, "_instance"):
                    Dispatcher._instance = object.__new__(cls)
        return Dispatcher._instance

    def __init__(self):
        pass

    def send(self, msg: message.Message):
        key = str(msg.type)
        if key in self._in_progress:
            self._in_progress_mutex.acquire()
            msg2 = self._in_progress[key]
            if msg2.result == 100:
                raise Exception("robot is already performing action")
            self._in_progress_mutex.release()
        self._in_progress[key] = msg

    def recv(self, msg: message.Message):
        key = str(msg.type)
        if key in self._in_progress:
            self._in_progress_mutex.acquire()
            self._in_progress[key].result = msg.result
            self._in_progress[key].dataint = msg.dataint
            self._in_progress[key].datastr = msg.datastr
            self._in_progress_mutex.release()

    def get_msg(self, type: int) -> message.Message:
        return self._in_progress[str(type)]

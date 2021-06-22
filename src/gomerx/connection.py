from logging import log
import threading
import os
from ctypes import *
from queue import Queue
from gomerx import protocol
from gomerx.exceptions import NoDevicesFound
from . import logger
import json


class Connection(object):
    _instance_lock = threading.Lock()
    _yuv_queue = Queue()
    _msg_queue = Queue()

    @CFUNCTYPE(c_int, POINTER(c_ubyte), c_int, c_int)
    def receive_video_data(yuv_data, w, h):
        yuv = string_at(yuv_data, int(w * h * 3 / 2))
        Connection._yuv_queue.put_nowait(yuv)
        return 0

    @CFUNCTYPE(c_int, c_char_p, c_int)
    def receive_msg(msg, len):
        Connection._msg_queue.put(msg)
        return 0

    def __new__(cls, *args, **kwargs):
        if not hasattr(Connection, '_instance'):
            with Connection._instance_lock:
                if not hasattr(Connection, '_instance'):
                    Connection._instance = object.__new__(cls)
        return Connection._instance

    def __init__(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        lib = os.path.join(dir, 'lib', 'libglproto64.dll')
        self._lib = CDLL(lib)

    def _search(self, name: str):
        name_p = c_char_p(name.encode())
        res = self._lib.ProtocolSearchOneDevice(name_p)
        if res != 1:
            raise NoDevicesFound()

    def connect(self, name: str):
        self._search(name)
        name_p = c_char_p(name.encode())
        res = self._lib.ProtocolConnectDevice(name_p, self.receive_msg)
        if res == 1:
            return True
        else:
            return False

    def destroy(self):
        res = self._lib.ProtocolDestroyConnect()
        if res == 0:
            return

    def send_msg(self, msg: str):
        msg_buf = create_string_buffer(msg.encode())
        self._lib.ProtocolSendMessage(msg_buf)

    def open_video(self):
        self._lib.ProtocolOpenVideo(self.receive_video_data)

    def close_video(self):
        self._lib.ProtocolCloseVideo()

    def recv(self):
        if not self._msg_queue.empty():
            msg_buf = self._msg_queue.get()
            msg = protocol.decode_msg(msg_buf)
            msg_dict = json.loads(msg_buf)
            if 'code' in msg_dict:
                if msg_dict['code'] == 102:
                    msg_dict['code'] = 100
                    msg_dict['msgtype'] = 2
                    self.send_msg(json.dumps(msg_dict))
            if not msg:
                logger.warn("[Conn] recv, decode msg is None")
                return None
            else:
                if isinstance(msg, protocol.Message):
                    if not msg.unpack_protocol():
                        logger.warn("[Conn] recv, unpack failed")
                    return msg

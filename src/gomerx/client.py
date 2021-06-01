import threading
from . import connection
from . import protocol
from . import logger
from . import event
import time

CLIENT_MAX_EVENT_NUM = 16


class EventIdentify(object):
    def __init__(self):
        self._valid = False
        self._ident = None
        self._event = threading.Event()


class MsgHandler(object):
    def __init__(self, proto_data=None, req_cb=None, ack_cb=None):
        self._proto_data = proto_data
        self._req_cb = req_cb
        self._ack_cb = ack_cb

    @property
    def proto_data(self):
        return self._proto_data

    @staticmethod
    def make_dict_key(msg: protocol.Message):
        return msg._seq_id


class Client(object):
    def __init__(self, conn=None, name=None):
        self._has_sent = 0
        self._has_recv = 0
        self._unpack_failed = 0
        self._running = False
        self._thread = None
        self._wait_ack_list = {}
        self._handler_dict = {}
        self._dispatcher = event.Dispatcher()
        self._wait_ack_mutex = threading.Lock()
        self._conn = conn
        if self._conn is None:
            self._conn = connection.Connection()
        self._name = name
        self._video_enable = False
        self._event_list = []
        for i in range(0, CLIENT_MAX_EVENT_NUM):
            ident = EventIdentify()
            self._event_list.append(ident)

    def __del__(self):
        self.stop()

    @staticmethod
    def _make_ack_identify(msg: protocol.Message):
        if msg._is_ack:
            pass
        else:
            pass
        return str(msg._seq_id)

    def _ack_register_identify(self, msg: protocol.Message):
        self._wait_ack_mutex.acquire()
        ident = self._make_ack_identify(msg)
        self._wait_ack_list[ident] = 1
        self._wait_ack_mutex.release()
        evt = None
        for i, evt_ident in enumerate(self._event_list):
            if not evt_ident._valid:
                evt = evt_ident
                break
        if evt is None:
            logger.error("[Client] event list is run out")
            return None
        evt._valid = True
        evt._ident = ident
        evt._event.clear()
        return evt

    def _ack_unregister_identify(self, identify):
        try:
            self._wait_ack_mutex.acquire()
            if identify in self._wait_ack_list.keys():
                return self._wait_ack_list.pop(identify)
            else:
                logger.warning(
                    "[Client] cannot find ident {} in wait_ack_list".format(identify))
                return None
        finally:
            self._wait_ack_mutex.release()

    def _recv_task(self):
        self._running = True
        while self._running:
            msg = self._conn.recv()
            if not self._running:
                break
            if msg is None:
                time.sleep(0.5)
                continue
            self._has_recv += 1
            self._dispatch_to_send_sync(msg)
            self._dispatch_to_callback(msg)
            if self._dispatcher:
                self._dispatcher.dispatch(msg)

        self._running = False

    def _dispatch_to_send_sync(self, msg: protocol.Message):
        if msg._is_ack:
            ident = self._make_ack_identify(msg)
            self._wait_ack_mutex.acquire()
            if ident in self._wait_ack_list.keys():
                print("ident in keys")
                for i, evt in enumerate(self._event_list):
                    if evt._ident == ident and evt._valid:
                        self._wait_ack_list[ident] = msg
                        evt._event.set()
            else:
                pass
                # print("not in keys: ", self._wait_ack_list.keys())
            self._wait_ack_mutex.release()

    def _dispatch_to_callback(self, msg):
        key = MsgHandler.make_dict_key(msg)
        if msg._is_ack:
            if key in self._handler_dict.keys():
                self._handler_dict[key]._ack_cb(self, msg)
        else:
            if key in self._handler_dict.keys():
                self._handler_dict[key]._req_cb(self, msg)

    def add_handler(self, obj, name, f):
        self._dispatcher.add_handler(obj, name, f)

    def start(self):
        self._conn.connect(self._name)
        self._thread = threading.Thread(target=self._recv_task)
        self._thread.setDaemon(True)
        self._thread.start()

    def stop(self):
        if self._thread is not None and self._thread.is_alive():
            self._running = False
            # self._thread.join()
        if self._conn:
            self._conn.destroy()

    def send(self, data: str):
        self._conn.send_msg(data)

    def send_msg(self, msg: protocol.Message):
        data = msg.pack()
        self._has_sent += 1
        self.send(data)

    def resp_msg(self, msg):
        pass

    def send_sync_msg(self, msg: protocol.Message, callback=None, timeout=3):
        if not self._running:
            logger.error("[Client] send_sync_msg, rect_task is not running")
            return None
        if msg._need_ack > 0:
            evt = self._ack_register_identify(msg)
            if evt is None:
                logger.error("[Client] send_sync_msg, ack_register failed")
                return None
            self.send_msg(msg)
            evt._event.wait(timeout)
            if not evt._event.is_set():
                logger.error("[Client] send_sync_msg, evt not set, timeout")
                evt._valid = False
                return None
            resp_msg = self._ack_unregister_identify(evt._ident)
            evt._valid = False
            if resp_msg is None:
                logger.error("[Client] send_sync_msg, get resp msg failed.")
            else:
                if isinstance(resp_msg, protocol.Message):
                    try:
                        resp_msg.unpack_protocol()
                        if callback:
                            callback(resp_msg)
                    except Exception as e:
                        self._unpack_failed += 1
                        logger.warn("[Client] send_sync_msg, unpack failed")
                        return None
                else:
                    logger.warn(
                        "[Client] send_sync_msg, resp_msg instance error")
                    return None

            return resp_msg
        else:
            print("else send msg")
            self.send_msg(msg)

    def send_async_msg(self, msg: protocol.Message):
        if not self._running:
            return None
        msg._need_ack = 0
        return self.send_msg(msg)

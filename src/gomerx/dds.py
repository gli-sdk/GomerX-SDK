import time
import collections
import threading
from queue import Queue
from abc import abstractmethod
from . import logger
from . import module
from . import protocol


DDS_SUB_TYPE_PERIOD = 0

registered_subjects = {}


class _AutoRegisterSubject(type):
    '''hepler to automatically register Proto Class whereever they're defined '''

    def __new__(mcs, name, bases, attrs, **kw):
        return super().__new__(mcs, name, bases, attrs, **kw)

    def __init__(cls, name, bases, attrs, **kw):
        super().__init__(name, bases, attrs, **kw)
        if name == 'Subject':
            return
        key = name
        if key in registered_subjects.keys():
            raise ValueError("Duplicate Subject class {0}".format(name))
        registered_subjects[key] = cls


class Subject(metaclass=_AutoRegisterSubject):
    name = 'Subject'
    _push_proto_cls = protocol.ProtoPushPeriodMsg
    type = DDS_SUB_TYPE_PERIOD


class Subscriber(module.Module):
    def __init__(self, robot):
        super().__init__(robot)
        self.msg_sub_dict = {}
        self._publisher = collections.defaultdict(list)
        self._msg_queue = Queue()
        self._dispatcher_running = False
        self._dispatcher_thread = None

    def __del__(self):
        self.stop()

    def start(self):
        self._dds_mutex = threading.Lock()

    def stop(self):
        self._dispatcher_running = False
        if self._dispatcher_thread:
            self._msg_queue.put(None)
            self._dispatcher_thread.join()
            self._dispatcher_thread = None

    def add_subject_event_info(self, subject, callback=None, *args):
        pass

    def del_subject_event_info(self, subject):
        pass

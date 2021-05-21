import threading
from . import protocol
from . import logger

__all__ = ['Action, ActionDispatcher']

ACTION_IDLE = 'action_idle'
ACTION_RUNNING = 'action_running'
ACTION_SUCCEEDED = 'action_succeeded'
ACTION_FAILED = 'action_failed'


SDK_FIRST_ACTION_ID = 1
SDK_LAST_ACTION_ID = 10

registered_actions = {}


class _AutoRegisterAction(type):
    def __new__(mcs, name, bases, attrs, **kw):
        return super().__new__(mcs, name, bases, attrs, **kw)

    def __init__(cls, name, bases, attrs, **kw):
        super().__init__(name, bases, attrs, **kw)
        if name == 'Action':
            return
        key = name
        if key in registered_actions.keys():
            raise ValueError('duplicate proto class')
        if attrs['_action_proto_cls'] is None:
            raise ValueError('action must specific proto class')
        registered_actions[key] = cls


class Action(metaclass=_AutoRegisterAction):
    _action_mutex = threading.Lock()
    _next_action_id = SDK_FIRST_ACTION_ID

    def __init__(self, **kw):
        super().__init__(**kw)
        self._action_id = -1
        self._state = ACTION_IDLE

        self._event = threading.Event()
        self._obj = None
        self._on_state_changed = None

    def _get_next_action_id(self):
        self.__class__._action_mutex.acquire()
        action_id = self.__class__._next_action_id
        if self.__class__._next_action_id == SDK_LAST_ACTION_ID:
            self.__class__._next_action_id = SDK_FIRST_ACTION_ID
        else:
            self.__class__._next_action_id += 1
        self.__class__._action_mutex.release()
        return action_id

    @property
    def state(self):
        return self._state

    @property
    def is_running(self):
        return self._state is ACTION_RUNNING

    @property
    def is_completed(self):
        return self._state is ACTION_FAILED or self._state is ACTION_SUCCEEDED

    @property
    def has_succeeded(self):
        return self._state is ACTION_SUCCEEDED

    @property
    def has_failed(self):
        return self._state is ACTION_FAILED

    def _change_to_state(self, state):
        if state != self._state:
            origin = self._state
            self._state = state
            if self._on_state_changed and self._obj:
                self._on_state_changed(self._obj, self, origin, self._state)
            if self.is_completed:
                self._event.set()

    def make_action_key(self):
        return str(self._action_proto_cls._cmdid) + '-' + str(self._action_id)

    def wait_for_completed(self, timeout=None):
        if self._event.is_set() and self.is_completed:
            return True
        self._event.wait(timeout)
        if not self._event.is_set():
            self._event = ACTION_FAILED
            return False
        return True

    def _update_action_state(self, proto_state):
        if proto_state == 100:
            self._change_to_state(ACTION_RUNNING)
        elif proto_state == 101:
            self._change_to_state(ACTION_FAILED)
        elif proto_state == 102:
            self._change_to_state(ACTION_SUCCEEDED)

    def encode(self):
        raise NotImplementedError()

    def found_proto(self, proto):
        if proto.cmdid == self._action_proto_cls._cmdid:
            return True
        else:
            return False


class ActionDispatcher(object):
    def __init__(self, client=None):
        self._client = client
        self._in_progress_mutex = threading.Lock()
        self._in_progress = {}

        self._client.add_handler(self, 'ActionDispatcher', self._on_recv)

    @property
    def has_in_progress_actions(self):
        return len(self._in_progress) > 0

    @classmethod
    def _on_action_state_changed(cls, self, action, origin, target):
        if action.is_completed:
            action_key = action.make_action_key()
            self._in_progress_mutex.acquire()
            if action_key in self._in_progress.keys():
                del (self._in_progress[action_key])
            else:
                logger.warn("del failed")
            self._in_progress_mutex.release()

    @classmethod
    def _on_recv(cls, self, msg):
        proto = msg.get_proto()
        if proto is None:
            return
        action = None
        found_proto = False

        self._in_progress_mutex.acquire()
        for key in self._in_progress.keys():
            action = self._in_progress[key]
            if action:
                if action.found_proto(proto):
                    found_proto = True
                    break
            else:
                logger.warn("in_progress action is None")
        self._in_progress_mutex.release()

        if found_proto:
            if proto._code == 100:
                action._change_to_state(ACTION_RUNNING)
            elif proto._code == 101:
                action._change_to_state(ACTION_FAILED)
            elif proto._code == 102:
                action._change_to_state(ACTION_SUCCEEDED)

    def get_msg_by_action(self, action: Action):
        proto = action.encode()
        action_msg = protocol.Message(proto)
        return action_msg

    def send_action(self, action: Action):
        action._action_id = action._get_next_action_id()
        if self.has_in_progress_actions:
            logger.error("robot is already performing action")
            raise Exception("robot is already performing action")
        if action.is_running:
            raise Exception("action is running")

        action_msg = self.get_msg_by_action(action)
        action_key = action.make_action_key()
        self._in_progress[action_key] = action
        self._client.add_handler(self, "ActionDispatcher", self._on_recv)
        action._obj = self
        action._on_state_changed = self._on_action_state_changed
        self._client.send_msg(action_msg)

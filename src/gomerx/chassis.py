import threading
from . import action
from . import protocol
from . import robot
from . import module


class ChassisAction(action.Action):
    _action_proto_cls = protocol.ProtoChassisMove

    def __init__(self, x=0, y=0, a=0, **kw):
        super().__init__(**kw)
        self._x = x
        self._y = y
        self._a = a

    def encode(self):
        proto = protocol.ProtoChassisMove()
        proto._x = self._x
        proto._y = self._y
        proto._a = self._a
        return proto


class Chassis(module.Module):
    def __init__(self, robot):
        super().__init__(robot)
        self._action_dispatcher = robot.action_dispatcher
        self._auto_timer = None

    def _auto_stop_timer(self):
        self.drive_wheels(0, 0, 0, 0)

    def drive_wheels(self, lf=0, lb=0, rf=0, rb=0, timeout=None):
        """ 设置麦轮转速
        """
        proto = protocol.ProtoSetWheelSpeed()
        proto._lf = lf
        proto._lb = lb
        proto._rf = rf
        proto._rb = rb
        if timeout:
            if self._auto_timer:
                if self._auto_timer.is_alive():
                    self._auto_timer.cancel()
                self._auto_timer = threading.Timer(
                    timeout, self._auto_stop_timer)
                self._auto_timer.start()
                return self._send_sync_proto(proto)
        return self._send_async_proto(proto)

    def move(self, x=0, y=0, a=0, wait_for_complete=True):
        action = ChassisAction(x, y, a)
        self._action_dispatcher.send_action(action)
        if wait_for_complete:
            return action.wait_for_completed()
        return True

from . import protocol
from . import robot
from . import action
from . import module

__all__ = ['Arm']


class ArmAction(action.Action):
    _action_proto_cls = protocol.ProtoArmControl

    def __init__(self, x, y, **kw):
        super().__init__(**kw)
        self._x = x
        self._y = y

    def encode(self):
        proto = protocol.ProtoArmControl()
        proto._x = self._x
        proto._y = self._y
        return proto


class Arm(module.Module):
    def __init__(self, robot):
        super().__init__(robot)
        self._action_dispatcher = robot.action_dispatcher

    def move_to(self, x=0, y=0, wait_for_complete=True):
        action = ArmAction(x, y)
        self._action_dispatcher.send_action(action)
        if wait_for_complete:
            return action.wait_for_completed()
        return True

    def recenter(self, wait_for_complete=True):
        return self.move_to(12, 15, wait_for_complete)

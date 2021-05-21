from . import module
from . import protocol
from . import action

__all__ = ['Gripper']


class GripperAction(action.Action):
    _action_proto_cls = protocol.ProtoGripperCtrl

    def __init__(self, angle, **kw):
        super().__init__(**kw)
        self._value = angle

    def encode(self):
        proto = protocol.ProtoGripperCtrl()
        proto._value = self._value
        return proto


class Gripper(module.Module):
    def __init__(self, robot):
        super().__init__(robot)
        self._action_dispatcher = robot.action_dispatcher

    def _set_angle(self, angle, wait_for_complete=True):
        action = GripperAction(angle)
        self._action_dispatcher.send_action(action)
        if wait_for_complete:
            return action.wait_for_completed()
        return True

    def open(self, wait_for_complete=True) -> bool:
        return self._set_angle(0, wait_for_complete)

    def close(self, wait_for_complete=True) -> bool:
        return self._set_angle(100, wait_for_complete)

    def get_status(self) -> int:
        proto = protocol.ProtoGripperStatus()
        msg = protocol.Message(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                status = proto._status
                return status
            else:
                return False
        except Exception as e:
            return False

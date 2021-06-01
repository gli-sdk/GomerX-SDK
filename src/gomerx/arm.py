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
        """ 机械臂移动到绝对位置

        :param int x: x轴坐标, 单位cm
        :param int y: y轴坐标, 单位cm
        :param bool wait_for_complete: 是否等待执行完成, 默认为 True
        :return: 机械臂是否移到绝对位置, 完成返回 True, 未完成返回 False
        :rtype: bool
        """
        action = ArmAction(x, y)
        self._action_dispatcher.send_action(action)
        if wait_for_complete:
            return action.wait_for_completed()
        return True

    def recenter(self, wait_for_complete=True):
        """机械臂回中

        :param bool wait_for_complete: 是否等待执行完成, 默认为 True
        :return: 机械臂回中是否完成, 完成返回 True, 否则返回 False
        :rtype: bool
        """
        return self.move_to(12, 15, wait_for_complete)

from . import protocol
from . import module
from . import action


class ServoAction(action.Action):
    _action_proto_cls = protocol.ProtoServoControl

    def __init__(self, id=0, angle=0, **kw):
        super().__init__(**kw)
        self._id = id
        self._value = angle
        self._angle = 0

    def encode(self):
        proto = protocol.ProtoServoControl()
        proto._id = self._id
        proto._value = self._value
        return proto


class Servo(module.Module):
    def __init__(self, robot):
        super().__init__(robot)
        self._action_dispatcher = robot.action_dispatcher

    def move_to(self, id=0, angle=0, wait_for_complete=True):
        """舵机移动到绝对位置

        :param int id: [0, 1], 0:左侧舵机, 1:右侧舵机
        :param int angle: [0 ~ 180], 舵机旋转角度, 单位(°)
        :param bool wait_for_complete: 是否等待执行完成
        :return: 舵机是否移到绝对位置, 移动成功返回 True, 否则返回 False
        :rtype: bool
        """
        # TODO: 抛出InvalidParameter异常
        action = ServoAction(id, angle)
        self._action_dispatcher.send_action(action)
        if wait_for_complete:
            return action.wait_for_completed()
        return True

    def get_angle(self, id=0):
        """获取舵机角度值

        :param int id: [0, 1], 0:左侧舵机, 1:右侧舵机
        :return: 舵机角度
        :rtype: int
        """
        # TODO: 抛出InvalidParameter异常
        proto = protocol.ProtoServoGetAngle()
        proto._id = id
        msg = protocol.Message(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                angle = proto._angle
                return angle
            else:
                return False
        except Exception as e:
            return False

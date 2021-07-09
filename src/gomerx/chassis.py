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
        """ 设置麦轮速度

        :param int lf: [-100 ~ 100], 左前轮
        :param int lb: [-100 ~ 100], 左后轮
        :param int rf: [-100 ~ 100], 右前轮
        :param int rb: [-100 ~ 100], 右后轮
        :param float timeout: [0 ~ inf], 超过指定时间未收到新指令则停止运动, 单位s
        :return: 设置麦轮速度, 设置成功返回 True, 设置失败返回 False
        :rtype: bool
        """
        # TODO: 抛出InvalidParameter异常
        if not(-100 < lf < 100) or not(-100 < lb < 100) or not(-100 < rf < 100) \
                or not(-100 < rb < 100) or not(timeout > 0):
            raise Exception("invalid parameter")
        proto = protocol.ProtoSetWheelSpeed()
        proto._lf = lf
        proto._lb = lb
        proto._rf = rf
        proto._rb = rb
        if timeout:
            if self._auto_timer:
                if self._auto_timer.is_alive():
                    self._auto_timer.cancel()
            self._auto_timer = threading.Timer(timeout, self._auto_stop_timer)
            self._auto_timer.start()
            return self._send_sync_proto(proto)
        return self._send_async_proto(proto)

    def move(self, x=0, y=0, a=0, wait_for_complete=True):
        """控制底盘运动当指定位置, 坐标轴原点为当前位置

        :param int x: [-160 ~ 160], x 轴向运动距离, 右为正值, 单位 cm
        :param int y: [-160 ~ 160], y 轴向运动距离, 前为正值, 单位 cm
        :param int a: [-180 ~ 180], z 轴旋转角度, 右为正值, 单位 °
        :param bool wait_for_complete: 是否等待执行完成, 默认为 True
        :return: 移动到指定位置返回 True, 否则返回 False
        :rtype: bool
        """

        if not(-160 <= x <= 160) or not(-160 <= y <= 160) or not(-180 <= a <= 180):
            raise Exception("invalid parameter")
        action = ChassisAction(x, y, a)
        self._action_dispatcher.send_action(action)
        if wait_for_complete:
            return action.wait_for_completed()
        return True

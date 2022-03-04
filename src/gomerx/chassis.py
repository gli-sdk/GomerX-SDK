import time
import threading
from . import module
from . import client
from . import event
from . import message


class Chassis(module.Module):
    def __init__(self, client: client.Client):
        super().__init__(client)
        self._auto_timer = None
        self._running = False

    def _auto_stop_timer(self, *args):
        timeout = args[0]
        time.sleep(timeout)
        self.stop()
        self._auto_timer = None

    def stop(self):
        if self._running:
            self.client.send(message.Message(
                message.ChassisWheel, [0, 0, 0, 0]))
            self._running = False

    def drive_wheels(self, lf: int = 0, lb: int = 0, rf: int = 0, rb: int = 0, timeout: int = 10):
        """ 设置麦轮速度

        :param int lf: [-100 ~ 100], 左前轮
        :param int lb: [-100 ~ 100], 左后轮
        :param int rf: [-100 ~ 100], 右前轮
        :param int rb: [-100 ~ 100], 右后轮
        :param float timeout: [1 ~ inf], 超过指定时间未收到新指令则停止运动, 单位s
        :return: 设置麦轮速度, 设置成功返回 True, 设置失败返回 False
        :rtype: bool
        """
        if abs(lf) > 100 or abs(lb) > 100 or abs(rf) > 100 or abs(rb) > 100:
            raise Exception("lf, lb, rf, rb,value error")
        if timeout:
            if self._auto_timer is None:
                self._auto_timer = threading.Thread(
                    target=self._auto_stop_timer, args=(timeout,))
                self._auto_timer.setDaemon(True)
                self._auto_timer.start()
        msg = message.Message(
            message.ChassisWheel, [lf, lb, rf, rb])
        self._running = True
        return self.send_msg(msg)

    def move(self, x: int = 0, y: int = 0, a: int = 0, wait_for_complete=True) -> bool:
        """控制底盘运动当指定位置, 坐标轴原点为当前位置

        :param int x: [-160 ~ 160], x 轴向运动距离, 右为正值, 单位 cm
        :param int y: [-160 ~ 160], y 轴向运动距离, 前为正值, 单位 cm
        :param int a: [-180 ~ 180], z 轴旋转角度, 右为正值, 单位 °
        :param bool wait_for_complete: 是否等待执行完成, 默认为 True
        :return: 移动到指定位置返回 True, 否则返回 False
        :rtype: bool
        """
        if abs(x) > 160 or abs(y) > 160 or abs(a) > 180:
            raise Exception("x,y,a,value error")
        msg = message.Message(message.ChassisXYA, [x, y, a])
        self.send_msg(msg)
        if wait_for_complete:
            event.Dispatcher().send(msg)
            move_result = 100
            while move_result == 100:
                time.sleep(0.1)
                move_result = event.Dispatcher().get_msg(message.ChassisXYA).result
            return (move_result == 102)
        return True

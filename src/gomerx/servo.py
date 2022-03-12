from . import module
from . import message
from . import event
import time


class Servo(module.Module):

    def move_to(self, id: int = 0, angle: int = 90, wait_for_complete=True) -> bool:
        """舵机移动到绝对位置

        :param int id: [0, 1], 0:左侧舵机, 1:右侧舵机
        :param int angle: [0 ~ 180], 舵机旋转角度, 单位(°)
        :param bool wait_for_complete: 是否等待执行完成
        :return: 舵机是否移到绝对位置, 移动成功返回 True, 否则返回 False
        :rtype: bool
        """
        if id < 0 or id > 1:
            raise Exception("id value error")
        elif id == 0:
            if angle < 85 or angle > 180:
                raise Exception("angle value error")
        else:
            if angle < 0 or angle > 110:
                raise Exception("angle value error")
        dataint = [0xff, 0xff]
        dataint[id] = angle
        msg = message.Message(message.ArmServoAngle, dataint)
        self.send_msg(msg)
        if wait_for_complete:
            event.Dispatcher().send(msg)
            result = 100
            while result == 100:
                time.sleep(0.1)
                result = event.Dispatcher().get_msg(str(message.ArmServoAngle)).result
            return (result == 102)
        return True

    def reset(self):
        """舵机恢复初始位置

        """
        self.move_to(id=0, angle=180, wait_for_complete=False)
        self.move_to(id=1, angle=70, wait_for_complete=False)
        time.sleep(1)

    def get_angle(self, id=0) -> int:
        """获取舵机角度值

        :param int id: [0, 1], 0:左侧舵机, 1:右侧舵机
        :return: 舵机角度
        :rtype: int
        """
        pass

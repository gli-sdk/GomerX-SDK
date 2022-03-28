from . import module
from . import message
from . import event
import time


class Arm(module.Module):

    def move_to(self, y: int = 0, z: int = 0, wait_for_complete=True) -> bool:
        """ 机械臂移动到绝对位置

        :param int y: 机械手中心距离车体前平面距离, 单位cm
        :param int z: 机械手中心距离地面高度, 单位cm
        :param bool wait_for_complete: 是否等待执行完成, 默认为 True
        :return: 机械臂是否移到绝对位置, 完成返回 True, 未完成返回 False
        :rtype: bool
        """
        if y < 10 or y > 20 or z < 3 or z > 21:
            raise Exception(" y, z, value error")
        msg = message.Message(message.ArmEndPos, [y, z])
        event.Dispatcher().send(msg)
        self.send_msg(msg)
        if wait_for_complete:
            result = 100
            while result == 100:
                time.sleep(0.1)
                result = event.Dispatcher().get_msg(str(message.ArmEndPos)).result
            return (result == 102)
        return True

    def recenter(self, wait_for_complete=True) -> bool:
        """机械臂回中

        :param bool wait_for_complete: 是否等待执行完成, 默认为 True
        :return: 机械臂回中是否完成, 完成返回 True, 否则返回 False
        :rtype: bool
        """
        return self.move_to(10, 13, wait_for_complete)

    def calibrate(self, wait_for_complete=True) -> bool:
        """机械臂标定

        :param bool wait_for_complete: 是否等待执行完成, 默认为 True
        :return: 机械臂标定是否完成, 完成返回 True, 否则返回 False
        :rtype: bool
        """
        msg = message.Message(message.ArmCalib)
        event.Dispatcher().send(msg)
        self.send_msg(msg)
        if wait_for_complete:
            result = 100
            while result == 100:
                time.sleep(0.1)
                result = event.Dispatcher().get_msg(str(message.ArmCalib)).result
            return (result == 102)
        return True

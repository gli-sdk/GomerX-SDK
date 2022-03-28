
from . import module
from . import client
from . import message
from . import event
import time


class Gripper(module.Module):
    def __init__(self, client: client.Client):
        super().__init__(client)

    def open(self, wait_for_complete=True) -> bool:
        """控制机械手打开

        :param bool wait_for_complete: 是否等待执行完成, 默认为 True
        :type wait_for_complete: bool
        :return: 机械手打开为 True, 否则为 False
        :rtype: bool
        """
        msg = message.Message(message.Gripper, [0])
        self.send_msg(msg)
        if wait_for_complete:
            event.Dispatcher().send(msg)
            gripper_result = 100
            while gripper_result == 100:
                time.sleep(0.1)
                gripper_result = event.Dispatcher().get_msg(message.Gripper).result
            return (gripper_result == 102)
        return True

    def close(self, wait_for_complete=True) -> bool:
        """控制机械手关闭

        :param bool wait_for_complete: 是否等待执行完成, 默认为 True
        :return: 机械手关闭为 True, 否则为 False
        :rtype: bool
        """
        msg = message.Message(message.Gripper, [1])
        self.send_msg(msg)
        if wait_for_complete:
            event.Dispatcher().send(msg)
            gripper_result = 100
            while gripper_result == 100:
                time.sleep(0.1)
                gripper_result = event.Dispatcher().get_msg(message.Gripper).result
            return (gripper_result == 102)
        return True

    def get_status(self) -> int:
        """获取机械手张开状态

        :return: 0:完全张开, 1:完全闭合, 2:中间状态
        :rtype: int
        """
        pass

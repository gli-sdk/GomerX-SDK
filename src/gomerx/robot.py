from .arm import Arm
from .skill import Skill
from .client import Client
from .camera import Camera
from .chassis import Chassis
from .gripper import Gripper
from .servo import Servo
from .led import Led


class Robot(object):

    def __init__(self, name: str, mode='ap'):
        self._name = name
        self._client = Client(name)
        self._camera = Camera(self._client)
        self._chassis = Chassis(self._client)
        self._gripper = Gripper(self._client)
        self._servo = Servo(self._client)
        self._skill = Skill(self._client)
        self._led = Led(self._client)
        self._arm = Arm(self.client)

    def __del__(self):
        self.chassis.stop()
        self.client.disconnect()

    def close(self):
        self.client.disconnect()

    @property
    def client(self):
        return self._client

    @property
    def camera(self):
        """ 获取相机对象 """
        return self._camera

    @property
    def chassis(self):
        """ 获取车体底盘对象 """
        return self._chassis

    @property
    def gripper(self):
        """ 获取机械手对象 """
        return self._gripper

    @property
    def skill(self):
        """ 获取技能对象 """
        return self._skill

    @property
    def servo(self):
        """ 获取舵机对象 """
        return self._servo

    @property
    def led(self):
        """ 获取Led灯对象 """
        return self._led

    @property
    def arm(self):
        """ 获取机械臂对象 """
        return self._arm

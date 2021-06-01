from . import connection
from . import action
from . import skill
from . import arm
from . import camera
from . import chassis
from . import gripper
from . import led
from . import protocol
from . import servo
from . import client
from . import config
from . import logger

__all__ = ['Robot']


class Robot(object):
    """ GomerX 机器人 """

    def __init__(self, name: str):
        self._name = name
        self._conn = connection.Connection()
        self._conf = config.gomerx_conf
        self._modules = {}
        self._client = client.Client(self._conn, self._name)
        self._action_dispatcher = action.ActionDispatcher(self._client)
        self._arm = arm.Arm(self)
        self._camera = camera.Camera(self)
        self._chassis = chassis.Chassis(self)
        self._gripper = gripper.Gripper(self)
        self._led = led.Led(self)
        self._servo = servo.Servo(self)
        self._skill = skill.Skill(self)
        self._client.start()

    def __del__(self):
        self.close()

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
    def arm(self):
        """ 获取机械臂对象 """
        return self._arm

    @property
    def skill(self):
        """ 获取技能对象 """
        return self._skill

    @property
    def led(self):
        return self._led

    @property
    def servo(self):
        """ 获取舵机对象 """
        return self._servo

    @property
    def action_dispatcher(self):
        return self._action_dispatcher

    @property
    def name(self):
        return self._name

    def close(self):
        """ 关闭机器人连接 """
        self._client.stop()

    def get_version(self):
        """ 获取机器人固件版本号

        :return: 如："1.0.0"
        :rtype: str
        """
        proto = protocol.ProtoGetHardInfo()
        msg = protocol.Message(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                return proto._version
            else:
                return None
        except Exception as e:
            return None

    def get_sn(self):
        """ 获取机器人序列号SN

        :return: SN字符串，如：GomerX2019010100A
        :rtype: str | None
        """
        proto = protocol.ProtoGetHardInfo()
        msg = protocol.Message(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                return proto._sn
            else:
                return None
        except Exception as e:
            return None

    def get_battery(self):
        """ 获取机器人电量 
        
        :return: [0 ~ 100], 返回机器人的剩余电量百分比
        :rtype: int
        """
        proto = protocol.ProtoGetHardInfo()
        msg = protocol.Message(proto)
        try:
            resp_msg = self._client.send_sync_msg(msg)
            if resp_msg:
                proto = resp_msg.get_proto()
                return proto._battery
            else:
                return None
        except Exception as e:
            return None

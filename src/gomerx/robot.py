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
from . import vision
from . import client
from . import config
from . import logger

__all__ = ['Robot']

MODULE_ARM = 'Arm'
MODULE_CAMERA = 'Camera'
MODULE_CHASSIS = 'Chassis'
MODULE_GRIPPER = 'Gripper'
MODULE_LED = 'Led'
MODULE_SERVO = 'Servo'
MODULE_VISION = 'Vision'


class Robot(object):
    def __init__(self, name: str):
        self._name = name
        self._conn = connection.Connection()
        self._conf = config.gomerx_conf
        self._modules = {}
        self._client = client.Client(self._conn, self._name)
        self._action_dispatcher = action.ActionDispatcher(self._client)
        # self._dds = dds.Subscriber(self)
        self._arm = arm.Arm(self)
        self._camera = camera.Camera(self)
        self._chassis = chassis.Chassis(self)
        self._gripper = gripper.Gripper(self)
        self._led = led.Led(self)
        self._servo = servo.Servo(self)
        self._vision = vision.Vision(self)
        self._skill = skill.Skill(self)

        # self._dds.start()
        self._client.start()

    def __del__(self):
        self.close()

    @property
    def client(self):
        return self._client

    @property
    def camera(self):
        return self._camera

    @property
    def chassis(self):
        return self._chassis

    @property
    def gripper(self):
        return self._gripper

    @property
    def arm(self):
        return self._arm

    @property
    def skill(self):
        return self._skill

    @property
    def led(self):
        return self._led

    @property
    def vision(self):
        return self._vision

    @property
    def servo(self):
        return self._servo

    @property
    def action_dispatcher(self):
        return self._action_dispatcher

    @property
    def name(self):
        return self._name

    def close(self):
        self._client.stop()
        # self._dds.stop()

    def get_version(self):
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

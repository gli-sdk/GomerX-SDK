from . import connection
from . import action
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
from . import dds

__all__ = ['Robot']

MODULE_ARM = 'Arm'
MODULE_CAMERA = 'Camera'
MODULE_CHASSIS = 'Chassis'
MODULE_GRIPPER = 'Gripper'
MODULE_LED = 'Led'
MODULE_SERVO = 'Servo'
MODULE_VISION = 'Vision'


class RobotBase(object):
    def __init__(self, client=None, conf=config.gomerx_conf):
        self._client = client
        self._conf = conf
        self._modules = {}


class Robot(RobotBase):
    def __init__(self, name: str):
        self._name = name
        self._conn = connection.Connection()
        super().__init__(client.Client(self._conn, self._name), config.gomerx_conf)
        self._action_dispatcher = action.ActionDispatcher(self._client)

        self._scan_modules()
        self._client.start()

    def __del__(self):
        self._client.stop()
        if self._client is not None:
            self._client.stop()

    @property
    def client(self):
        return self._client

    @property
    def camera(self):
        return self.get_module(MODULE_CAMERA)

    @property
    def chassis(self):
        return self.get_module(MODULE_CHASSIS)

    @property
    def gripper(self):
        return self.get_module(MODULE_GRIPPER)

    @property
    def arm(self):
        return self.get_module(MODULE_ARM)

    @property
    def led(self):
        return self.get_module(MODULE_LED)

    @property
    def vision(self):
        return self.get_module(MODULE_VISION)

    @property
    def servo(self):
        return self.get_module(MODULE_SERVO)

    @property
    def action_dispatcher(self):
        return self._action_dispatcher

    @property
    def name(self):
        return self._name

    @property
    def dds(self):
        return self._dds

    def _scan_modules(self):
        _arm = arm.Arm(self)
        _camera = camera.Camera(self)
        _chassis = chassis.Chassis(self)
        _gripper = gripper.Gripper(self)
        _led = led.Led(self)
        _servo = servo.Servo(self)
        _vision = vision.Vision(self)
        _dds = dds.Subscriber(self)
        _dds.start()

        self._modules[_arm.__class__.__name__] = _arm
        self._modules[_camera.__class__.__name__] = _camera
        self._modules[_chassis.__class__.__name__] = _chassis
        self._modules[_gripper.__class__.__name__] = _gripper
        self._modules[_led.__class__.__name__] = _led
        self._modules[_servo.__class__.__name__] = _servo
        self._modules[_vision.__class__.__name__] = _vision

    def get_module(self, name: str):
        return self._modules[name]

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

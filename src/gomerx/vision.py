from . import module
from . import protocol
from . import dds

__all__ = ['Vision', 'COLOR', 'FACE', 'LINE', 'MARKER', 'QRCODE']

COLOR = "color"
FACE = "face"
LINE = "line"
MARKER = "marker"
QRCODE = "qrcode"


class VisionPushEvent(dds.Subject):
    name = "vision_push"
    type = dds.DDS_SUB_TYPE_PERIOD

    def __init__(self):
        self._type = 0
        self._info = []

    @property
    def info(self):
        return self._info

    def decode(self, data):
        pass


class Vision(module.Module):
    def __init__(self, robot):
        self._robot = robot
        self.on_detect_event_cb = None

    @staticmethod
    def _id2marker(marker_id):
        return str(marker_id)

    @staticmethod
    def _type2info(det_type):
        if det_type == 1:
            return "face"

    def _enable_detection(self, name):
        proto = protocol.ProtoVisionDetectEnable()
        proto._name = name
        msg = protocol.Message(proto)
        try:
            resp_msg = self.client.send_sync_msg(msg)
            if resp_msg:
                return True
        except Exception as e:
            return False
        return True

    def _disable_detection(self, name):
        proto = protocol.ProtoVisionDetectEnable()
        msg = protocol.Message(proto)
        try:
            resp_msg = self.client.send_sync_msg(msg)
            if resp_msg:
                return True
        except Exception as e:
            return False
        return True

    def sub_detect_info(self, name, color=None, callback=None, *args, **kw):
        if name is COLOR:
            pass
        elif name is FACE:
            pass
        elif name is MARKER:
            pass
        elif name is LINE:
            pass
        elif name is QRCODE:
            pass
        else:
            return False

        result = self._enable_detection(name)
        if result:
            sub = self._robot.dds
            subject = VisionPushEvent()
            protocol.ProtoVisionDetectInfo()
            sub.add_subject_event_info(subject, callback, args, kw)
            return True
        else:
            return False

    def unsub_detect_info(self, name):
        return self._disable_detection(name)

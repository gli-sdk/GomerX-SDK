from . import action
from . import protocol
from . import robot
from . import module


class PatternDetAction(action.Action):
    _action_proto_cls = protocol.ProtoPatternDet

    def __init__(self, id, timeout, **kw):
        super().__init__(**kw)
        self._id = id
        self._timeout = timeout

    def encode(self):
        proto = protocol.ProtoPatternDet()
        proto._id = self._id
        proto._timeout = self._timeout
        return proto


class FaceDetAction(action.Action):
    _action_proto_cls = protocol.ProtoFaceDet

    def __init__(self, _id, timeout, **kw):
        super().__init__(**kw)
        self._id = -1
        self._timeout = timeout

    def encode(self):
        proto = protocol.ProtoFaceDet()
        proto._id = self._id
        proto._timeout = self._timeout
        return proto


class ColorDetAction(action.Action):
    _action_proto_cls = protocol.ProtoColorDet

    def __init__(self, hsv_low, hsv_high, timeout, **kw):
        super().__init__(**kw)
        self._hsv_low = hsv_low
        self._hsv_high = hsv_high
        self._timeout = timeout

    def encode(self):
        proto = protocol.ProtoColorDet()
        proto._hsv_low = self._hsv_low
        proto._hsv_high = self._hsv_high
        proto._timeout = self._timeout
        return proto


class LineDetAction(action.Action):
    _action_proto_cls = protocol.ProtoLineDet

    def __init__(self, hsv_low, hsv_high, timeout, **kw):
        super().__init__(**kw)
        self._hsv_low = hsv_low
        self._hsv_high = hsv_high
        self._timeout = timeout

    def encode(self):
        proto = protocol.ProtoLineDet()
        proto._hsv_low = self._hsv_low
        proto._hsv_high = self._hsv_high
        proto._timeout = self._timeout
        return proto


class QrCodeDetAction(action.Action):
    _action_proto_cls = protocol.ProtoQrCodeDet

    def __init__(self, timeout, **kw):
        super().__init__(**kw)
        self._timeout = timeout

    def encode(self):
        proto = protocol.ProtoQrCodeDet()
        proto._timeout = self._timeout
        return proto


class PatternTrackAction(action.Action):
    _action_proto_cls = protocol.ProtoPatternTrack

    def __init__(self, id, x, y, **kw):
        super().__init__(**kw)
        self._id = id
        self._x = x
        self._y = y

    def encode(self):
        proto = protocol.ProtoPatternTrack()
        proto._id = self._id
        proto._x = self._x
        proto._y = self._y
        return proto


class LineTrackAction(action.Action):
    _action_proto_cls = protocol.ProtoLineTrack

    def __init__(self, id, **kw):
        super().__init__(**kw)
        self._id = id

    def encode(self):
        proto = protocol.ProtoLineTrack()
        proto._id = self._id
        return proto


class Skill(module.Module):
    def __init__(self, robot):
        super().__init__(robot)
        self._action_dispatcher = robot.action_dispatcher
        self._auto_timer = None

    @staticmethod
    def _hsv_in_cv(hsv=(0, 0, 0)):
        h = round(hsv[0] / 2)
        s = round(hsv[1] * 2.55)
        v = round(hsv[2] * 2.55)
        return (h, s, v)

    def detect_face(self, timeout=1):
        action = FaceDetAction(-1, timeout)
        self._action_dispatcher.send_action(action)
        return action.wait_for_completed()

    def detect_pattern(self, id='A', timeout=1):
        action = PatternDetAction(id, timeout)
        self._action_dispatcher.send_action(action)
        return action.wait_for_completed()

    def detect_qrcode(self, timeout=1):
        action = QrCodeDetAction(timeout)
        self._action_dispatcher.send_action(action)
        result = action.wait_for_completed()
        data = action._data
        return result, data

    def move_to_pattern(self, id='A', x=0, y=13):
        action = PatternTrackAction(id, x, y)
        self._action_dispatcher.send_action(action)
        return action.wait_for_completed()

    def detect_color_blob(self, hsv_low=(0, 0, 0), hsv_high=(360, 100, 100), timeout=1):
        _hsv_low = self.__class__._hsv_in_cv(hsv_low)
        _hsv_high = self.__class__._hsv_in_cv(hsv_high)

        action = ColorDetAction(_hsv_low, _hsv_high, timeout)
        self._action_dispatcher.send_action(action)
        result = action.wait_for_completed()
        data = action._data
        if data is not None:
            data[0] = int(data[0] / 2)
            data[1] = int(data[1] / 2)
            data[2] = int(data[2] / 2)
            data[3] = int(data[3] / 2)
        return result, data

    def detect_line(self, hsv_low=(0, 0, 0), hsv_high=(360, 100, 100), timeout=1):
        _hsv_low = self.__class__._hsv_in_cv(hsv_low)
        _hsv_high = self.__class__._hsv_in_cv(hsv_high)

        action = LineDetAction(_hsv_low, _hsv_high, timeout)
        self._action_dispatcher.send_action(action)
        result = action.wait_for_completed()
        data = action._data
        if data is not None:
            data[0] = int(data[0] / 2)
            data[1] = int(data[1] / 2)
            data[2] = int(data[2] / 2)
            data[3] = int(data[3] / 2)
        return result, data

    def move_along_line(self):
        action = LineTrackAction(0)
        self._action_dispatcher.send_action(action)
        return action.wait_for_completed()

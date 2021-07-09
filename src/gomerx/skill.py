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
        """ 检测人脸

        :param int timeout: 超时时间，单位 s
        :return: 检测到人脸返回True，未检测到返回False
        """
        action = FaceDetAction(-1, timeout)
        self._action_dispatcher.send_action(action)
        return action.wait_for_completed()

    def detect_pattern(self, id='A', timeout=1):
        """ 检测图案

        :param str id: 图案名称，支持'A'~'Z', '0'~'9'
        :param int timeout: 超时时间，单位 s
        :return: 检测到指定图案返回True，未检测到返回False
        """
        if not id.isupper() and not id.isdigit():
            raise Exception('invalid parameter')
        action = PatternDetAction(id, timeout)
        self._action_dispatcher.send_action(action)
        return action.wait_for_completed()

    def detect_qrcode(self, timeout=1):
        """ 检测二维码

        :param int timeout: 超时时间，单位 s
        :return: result (bool) - 检测到二维码返回True，未检测到返回False \n
                 data (str) - result为True时，返回二维码字符串信息
        """
        action = QrCodeDetAction(timeout)
        self._action_dispatcher.send_action(action)
        result = action.wait_for_completed()
        data = action._data
        return result, data

    def move_to_pattern(self, id='A', x=0, y=13):
        """ 移动至图案前指定位置

        :param str id: 图案名称，支持'A'~'Z', '0'~'9'
        :param int x: 停止时，图案中心线与机器人中心线左右距离, 范围[-30, 30], 图案在机器人右侧为正，单位cm
        :param int y: 停止时，图案处于机器人摄像头平面前方距离, 范围[13, 60], 单位cm
        :return: 成功移动到图案前指定位置返回True，失败返回False
        """

        if not id.isupper() and not id.isdigit():
            raise Exception('invalid parameter')
        if not(-30 <= x <= 30) or not(13 <= y <= 60):
            raise Exception('invalid parameter')
        action = PatternTrackAction(id, x, y)
        self._action_dispatcher.send_action(action)
        return action.wait_for_completed(timeout=30)

    def detect_color_blob(self, hsv_low=(0, 0, 0), hsv_high=(360, 100, 100), timeout=1):
        """ 检测色块

        :param tuple hsv_low: hsv颜色下边界
        :param tuple hsv_high: hsv颜色上边界
        :param int timeout: 超时时间，单位 s
        :return: result (bool) - 检测到色块返回True，未检测到返回False \n
                 data (list) - result为True时，返回色块中心坐标及宽高[x, y, w, h]
        """

        if not(0 < hsv_low[0] < 360) or not(0 < hsv_low[1] < 100) or not(0 < hsv_low[2] < 100) \
                or not(0 < hsv_high[0] < 360) or not(0 < hsv_high[1] < 100) \
                or not(0 < hsv_high[2] < 100) or not(timeout > 0):
            raise Exception('invalid parameter')
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
        """ 检测线段

        :param tuple hsv_low: hsv颜色下边界
        :param tuple hsv_high: hsv颜色上边界
        :param int timeout: 超时时间，单位 s
        :return: result (bool) - 检测到线段返回True，未检测到返回False \n
                 data (list) - result为True时，返回线段起点和终点坐标[x0, y0, x1, y1]
        """

        if not(0 < hsv_low[0] < 360) or not(0 < hsv_low[1] < 100) or not(0 < hsv_low[2] < 100) \
                or not(0 < hsv_high[0] < 360) or not(0 < hsv_high[1] < 100) \
                or not(0 < hsv_high[2] < 100) or not(timeout > 0):
            raise Exception('invalid parameter')
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
        """ 自动巡线直到线段消失，使用前需先使用detect_line方法

        :return: 巡线结束返回True，异常返回False
        """
        action = LineTrackAction(0)
        self._action_dispatcher.send_action(action)
        return action.wait_for_completed(timeout=60)

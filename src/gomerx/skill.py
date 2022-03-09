import time
from . import module
from . import message
from . import event

LINE_END = 'end'
LINE_CROSS = 'cross'
ROAD_TYPE = {'end': 0, 'cross': 1}


class Skill(module.Module):

    @staticmethod
    def _hsv_in_cv(hsv=(0, 0, 0)):
        h = round(hsv[0] / 2)
        s = round(hsv[1] * 2.55)
        v = round(hsv[2] * 2.55)
        return (h, s, v)
    PATTERN_STR = ('0', '1', '2', '3', '4', '5', '6',
                   '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')

    def detect_face(self, timeout: int = 1) -> tuple:
        """ 检测人脸

        :param int timeout: 超时时间, 单位 s
        :return: 检测到人脸返回True, 未检测到返回False
        """
        msg = message.Message(
            message.DetFace, [timeout])
        self.send_msg(msg)
        event.Dispatcher().send(msg)
        detface_result = 100
        while detface_result == 100:
            time.sleep(0.1)
            detface_result = event.Dispatcher().get_msg(message.DetFace).result
        if detface_result == 102:
            face_result = event.Dispatcher().get_msg(message.DetFace).dataint
            print(face_result)
            return True, face_result
        else:
            return False, []

    def recognize_face(self) -> tuple:
        """ 识别检测到的人脸身份

        :return: result (bool) - 识别出人脸身份为True, 未识别出为False
                 name (str) - 人脸姓名
        """
        return False, ''

    def save_face(self, name: str) -> bool:
        """ 录入人脸

        :param str name: 待录入人脸的姓名
        :return: 录入成功返回True, 失败返回False
        """
        return False

    def delete_face(self, name: str) -> bool:
        """ 删除人脸

        :param str name: 待删除人脸的姓名
        :return: 删除成功返回True, 失败返回False
        """
        return False

    def get_face_list(self) -> tuple:
        """ 获取已保存的人脸列表

        :param list face_list
        :return: result (bool) - 获取成功返回True, 失败返回False
                 data (list) - 包含人脸编号和姓名的列表
        """
        return False, []

    def detect_pattern(self, id: str = 'A', timeout: int = 1) -> bool:
        """ 检测图案

        :param str id: 图案名称，支持'A'~'Z', '0'~'9'
        :param int timeout: 超时时间，单位 s
        :return: 检测到指定图案返回True, 未检测到返回False
        """
        if id not in Skill.PATTERN_STR:
            raise Exception("id value error")
        msg = message.Message(
            message.DetPattern, [timeout], id)
        self.send_msg(msg)
        event.Dispatcher().send(msg)
        detpattern_result = 100
        while detpattern_result == 100:
            time.sleep(0.1)
            detpattern_result = event.Dispatcher().get_msg(message.DetPattern).result
        return (detpattern_result == 102)

    def detect_qrcode(self, timeout: int = 1) -> tuple:
        """ 检测二维码

        :param int timeout: 超时时间，单位 s
        :return: result (bool) - 检测到二维码返回True, 未检测到返回False \n
                 data (str) - result为True时, 返回二维码字符串信息
        """
        msg = message.Message(
            message.DetQrCode, [timeout])
        self.send_msg(msg)
        event.Dispatcher().send(msg)
        detect_result = 100
        while detect_result == 100:
            time.sleep(0.1)
            detect_result = event.Dispatcher().get_msg(message.DetQrCode).result
        if detect_result == 102:
            qrcode_result = event.Dispatcher().get_msg(message.DetQrCode).datastr
            print(qrcode_result)
            return True, qrcode_result
        else:
            return False, ''

    def move_to_pattern(self, id: str = 'A', x: int = 0, y: int = 13) -> bool:
        """ 移动至图案前指定位置

        :param str id: 图案名称，支持'A'~'Z', '0'~'9'
        :param int x: 停止时，图案中心线与机器人中心线左右距离, 范围[-30, 30], 图案在机器人右侧为正，单位cm
        :param int y: 停止时，图案处于机器人摄像头平面前方距离, 范围[13, 60], 单位cm
        :return: 成功移动到图案前指定位置返回True, 失败返回False
        """
        if y < 13 or y > 60 or x > abs(round(0.4 * y)):
            raise Exception("x , y value error")
        if id not in Skill.PATTERN_STR:
            raise Exception("id value error")
        msg = message.Message(
            message.Move2Pattern, [x, y], id)
        self.send_msg(msg)
        event.Dispatcher().send(msg)
        detpattern_result = 100
        while detpattern_result == 100:
            time.sleep(0.1)
            detpattern_result = event.Dispatcher().get_msg(message.Move2Pattern).result
        return (detpattern_result == 102)

    def detect_color_blob(self, hsv_low: tuple = (0, 0, 0), hsv_high: tuple = (360, 100, 100), timeout: int = 1) -> tuple:
        """ 检测色块

        :param tuple hsv_low: hsv颜色下边界
        :param tuple hsv_high: hsv颜色上边界
        :param int timeout: 超时时间，单位 s
        :return: result (bool) - 检测到色块返回True, 未检测到返回False \n
                 data (list) - result为True时, 返回色块中心坐标及宽高[x, y, w, h]
        """
        if hsv_low[0] > hsv_high[0] or hsv_low[1] > hsv_high[1] or hsv_low[2] > hsv_high[2]:
            raise Exception("hsv value error")
        if min(hsv_low) < 0 or max(hsv_high) > 360:
            raise Exception("hsv value error")
        if hsv_high[1] > 100 or hsv_high[2] > 100:
            raise Exception("hsv value error")
        opencv_hsv_low = Skill._hsv_in_cv(hsv_low)
        opencv_hsv_high = Skill._hsv_in_cv(hsv_high)
        msg = message.Message(
            message.DetColor, [timeout, opencv_hsv_low[0], opencv_hsv_high[0], opencv_hsv_low[1], opencv_hsv_high[1], opencv_hsv_low[2], opencv_hsv_high[2]])
        self.send_msg(msg)
        event.Dispatcher().send(msg)
        detline_result = 100
        while detline_result == 100:
            time.sleep(0.1)
            detline_result = event.Dispatcher().get_msg(message.DetColor).result
        if detline_result == 102:
            color_coordinate = event.Dispatcher().get_msg(message.DetColor).dataint
            return True, color_coordinate
        else:
            return False, []

    def detect_line(self, hsv_low: tuple = (0, 0, 0), hsv_high: tuple = (360, 100, 100), timeout: int = 1) -> tuple:
        """ 检测线段

        :param tuple hsv_low: hsv颜色下边界
        :param tuple hsv_high: hsv颜色上边界
        :param int timeout: 超时时间，单位 s
        :return: result (bool) - 检测到线段返回True, 未检测到返回False \n
                 data (list) - result为True时, 返回线段起点和终点坐标[x0, y0, x1, y1]
        """
        if hsv_low[0] > hsv_high[0] or hsv_low[1] > hsv_high[1] or hsv_low[2] > hsv_high[2]:
            raise Exception("hsv value error")
        if min(hsv_low) < 0 or max(hsv_high) > 360:
            raise Exception("hsv value error")
        if hsv_high[1] > 100 or hsv_high[2] > 100:
            raise Exception("hsv value error")
        opencv_hsv_low = Skill._hsv_in_cv(hsv_low)
        opencv_hsv_high = Skill._hsv_in_cv(hsv_high)
        msg = message.Message(
            message.DetLine, [timeout, opencv_hsv_low[0], opencv_hsv_high[0], opencv_hsv_low[1], opencv_hsv_high[1], opencv_hsv_low[2], opencv_hsv_high[2]])
        self.send_msg(msg)
        event.Dispatcher().send(msg)
        detline_result = 100
        while detline_result == 100:
            time.sleep(0.1)
            detline_result = event.Dispatcher().get_msg(message.DetLine).result
        if detline_result == 102:
            coordinate = event.Dispatcher().get_msg(message.DetLine).dataint
            return True, coordinate
        else:
            return False, []

    def move_along_line(self, stop=LINE_END) -> bool:
        """ 自动巡线直到线段消失, 使用前需先使用detect_line方法

        :return: 巡线结束返回True, 异常返回False
        """
        if stop not in ROAD_TYPE:
            raise Exception(" ROAD_TYPE error")
        msg = message.Message(
            message.FollowLine, [ROAD_TYPE[stop]])
        self.send_msg(msg)
        event.Dispatcher().send(msg)
        detline_result = event.Dispatcher().get_msg(message.FollowLine).result
        while detline_result == 100:
            time.sleep(0.1)
            detline_result = event.Dispatcher().get_msg(message.FollowLine).result
        if detline_result == 102:
            return True
        else:
            return False

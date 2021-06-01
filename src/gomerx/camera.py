import numpy as np
import cv2 as cv
import threading

from numpy.lib.shape_base import dsplit
from . import connection
from . import robot


class Camera(object):
    def __init__(self, robot):
        self._conn = robot._conn
        self._yuv = None
        self._video_enable = False

    def __del__(self):
        self.stop_video_stream()

    def start_video_stream(self, display=True):
        """ 开启视频流

        :param display: 是否显示视频, 默认为 True
        :type display: bool 
        :return: 视频流是否开启, 开启返回 True, 否则返回 False
        :rtype: bool
        """
        self._conn.open_video()
        self._video_enable = True
        video_thread = threading.Thread(
            target=self.handle_video_data, args=(display,))
        video_thread.setDaemon(True)
        video_thread.start()

    def stop_video_stream(self):
        """ 停止视频流

        :return: 视频流是否停止, 视频停止返回 True, 视频未停止返回 False
        :rtype: bool
        """
        if self._video_enable:
            self._conn.close_video()
            self._video_enable = False
            cv.destroyAllWindows()
            self._video_enable = False

    def read_cv_image(self):
        """读取一帧opencv-bgr格式的图片

        :return: 返回一张图片
        :rtype: numpy
        """
        if self._yuv:
            w = 800
            h = 600
            img_array = np.frombuffer(self._yuv, np.uint8)
            yuv = np.reshape(img_array, (int(h * 3 / 2), int(w)))
            img = cv.cvtColor(yuv, cv.COLOR_YUV2BGR_I420)
            return img

    def handle_video_data(self, display: bool):
        while self._video_enable:
            if not connection.Connection._yuv_queue.empty():
                self._yuv = connection.Connection._yuv_queue.get()
                if display:
                    img = self.read_cv_image()
                    cv.imshow("GomerX View", img)
                    cv.waitKey(27)

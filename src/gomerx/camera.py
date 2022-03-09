from ctypes import *
import os
import numpy as np
import cv2 as cv
from .client import Client
from .module import Module
from . import message


class Camera(Module):
    _yuv = None

    def __init__(self, client: Client):
        super().__init__(client)
        self._display = True
        dir = os.path.dirname(os.path.dirname(__file__))
        lib = os.path.join(dir, 'lib', 'libglproto64.dll')
        self._dll = CDLL(lib)

    @CFUNCTYPE(c_int, POINTER(c_ubyte), c_int, c_int)
    def recv_video_data(yuv_data, w, h):
        Camera._yuv = string_at(yuv_data, int(w * h * 3 / 2))
        return 0

    def start_video_stream(self, display=True):
        """ 开启视频流

        :param display: 是否显示视频, 默认为 True
        :type display: bool
        :return: 视频流是否开启, 开启返回 True, 否则返回 False
        :rtype: bool
        """
        self._display = display
        self.client.send(message.Message(message.Video, [1]))
        self._dll.CreateGvideo(self.recv_video_data)

    def stop_video_stream(self):
        """ 停止视频流

        :return: 视频流是否停止, 视频停止返回 True, 视频未停止返回 False
        :rtype: bool
        """
        self._dll.DestroyGvideo()
        self.client.send(message.Message(message.Video, [0]))

    def read_cv_image(self):
        """读取一帧opencv-bgr格式的图片

        :return: 返回一张图片, 分辨率为 800x600
        :rtype: numpy
        """
        img = None
        if Camera._yuv is not None:
            w = 800
            h = 600
            img_array = np.frombuffer(Camera._yuv, np.uint8)
            yuv = np.reshape(img_array, (int(h * 3 / 2), int(w)))
            img = cv.cvtColor(yuv, cv.COLOR_YUV2BGR_I420)
        return img

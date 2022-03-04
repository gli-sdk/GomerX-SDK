from .client import Client
from .module import Module


class Camera(Module):
    def __init__(self, client: Client):
        super().__init__(client)
        self._display = True

    def start_video_stream(self, display=True):
        """ 开启视频流

        :param display: 是否显示视频, 默认为 True
        :type display: bool
        :return: 视频流是否开启, 开启返回 True, 否则返回 False
        :rtype: bool
        """
        self._display = display
        self._client.open_video(self._display)

    def stop_video_stream(self):
        """ 停止视频流

        :return: 视频流是否停止, 视频停止返回 True, 视频未停止返回 False
        :rtype: bool
        """
        self._client.close_video(self._display)

    def read_cv_image(self):
        """读取一帧opencv-bgr格式的图片

        :return: 返回一张图片, 分辨率为 800x600
        :rtype: numpy
        """
        pass

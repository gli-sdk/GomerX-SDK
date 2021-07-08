import cv2 as cv
import numpy as np
from gomerx import robot


def get_track_bar_value(*args):
    # 滑动条的回调函数，获取滑动条位置处的值
    h_min = cv.getTrackbarPos(track_bar_h_min, WINDOW_NAME)
    h_max = cv.getTrackbarPos(track_bar_h_max, WINDOW_NAME)
    s_min = cv.getTrackbarPos(track_bar_s_min, WINDOW_NAME)
    s_max = cv.getTrackbarPos(track_bar_s_max, WINDOW_NAME)
    v_min = cv.getTrackbarPos(track_bar_v_min, WINDOW_NAME)
    v_max = cv.getTrackbarPos(track_bar_v_max, WINDOW_NAME)

    # 值的重映射
    h_min, h_max = 0.5*h_min, 0.5*h_max
    s_min, s_max = s_min*2.55, s_max*2.55
    v_min, v_max = v_min*2.55, v_max*2.55

    return h_min, h_max, s_min, s_max, v_min, v_max


def init_track_bar():
    # 初始化函数
    # 创建一个窗口，放置6个滑动条
    # h_min, h_max 范围 (0-360)
    # s_min, s_max, v_min, v_max 范围 (0-100)
    cv.namedWindow(WINDOW_NAME, 0)
    cv.resizeWindow(WINDOW_NAME, 1000, 800)
    cv.createTrackbar(track_bar_h_min, WINDOW_NAME,
                      97, 360, get_track_bar_value)
    cv.createTrackbar(track_bar_h_max, WINDOW_NAME,
                      232, 360, get_track_bar_value)
    cv.createTrackbar(track_bar_s_min, WINDOW_NAME,
                      30, 100, get_track_bar_value)
    cv.createTrackbar(track_bar_s_max, WINDOW_NAME,
                      60, 100, get_track_bar_value)
    cv.createTrackbar(track_bar_v_min, WINDOW_NAME,
                      35, 100, get_track_bar_value)
    cv.createTrackbar(track_bar_v_max, WINDOW_NAME,
                      60, 100, get_track_bar_value)


if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_camera = my_robot.camera
    my_camera.start_video_stream(display=False)

    # 确保得到视频流之后再显示窗口显示图片
    while True:
        img = my_camera.read_cv_image()
        if img is not None:
            break

    WINDOW_NAME = "Threshold Editor"
    track_bar_h_max = "H_max"
    track_bar_h_min = "H_min"
    track_bar_s_max = "S_max"
    track_bar_s_min = "S_min"
    track_bar_v_max = "V_max"
    track_bar_v_min = "V_min"

    # 窗口与滚动条的初始化
    init_track_bar()

    while True:
        img = my_camera.read_cv_image()
        img_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # 调用回调函数，获取滑动条的值
        h_min, h_max, s_min, s_max, v_min, v_max = get_track_bar_value(0)
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])

        # 获得指定颜色范围内的掩码
        mask = cv.inRange(img_HSV, lower, upper)

        # 单通道扩展为三通道
        mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)

        # 对阈值处理后的图和原图进行拼接
        composite_image = np.hstack((img, mask))

        # 显示最终结果
        cv.imshow(WINDOW_NAME, composite_image)

        # 按下 Esc 键退出程序
        if cv.waitKey(1) & 0xFF == 27:
            break

    cv.destroyAllWindows()
    my_camera.stop_video_stream()
    my_robot.close()

import cv2 as cv
import numpy as np
from gomerx import robot


# 滑动条的回调函数，获取滑动条位置处的值
def get_track_bar_value(*args):
    h_min = cv.getTrackbarPos(track_bar_h_min, window_name)
    h_max = cv.getTrackbarPos(track_bar_h_max, window_name)
    s_min = cv.getTrackbarPos(track_bar_s_min, window_name)
    s_max = cv.getTrackbarPos(track_bar_s_max, window_name)
    v_min = cv.getTrackbarPos(track_bar_v_min, window_name)
    v_max = cv.getTrackbarPos(track_bar_v_max, window_name)

    # 值的重映射
    h_min, h_max = 0.5*h_min, 0.5*h_max
    s_min, s_max = s_min*2.55, s_max*2.55
    v_min, v_max = v_min*2.55, v_max*2.55

    return h_min, h_max, s_min, s_max, v_min, v_max


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

    window_name = "TrackBars"
    track_bar_h_max = "H_max"
    track_bar_h_min = "H_min"
    track_bar_s_max = "S_max"
    track_bar_s_min = "S_min"
    track_bar_v_max = "V_max"
    track_bar_v_min = "V_min"

    # 创建一个窗口，放置6个滑动条
    # h_min, h_max 范围 (0-360)
    # s_min, s_max, v_min, v_max 范围 (0-100)

    cv.namedWindow(window_name, 0)
    cv.resizeWindow(window_name, 1000, 800)
    cv.createTrackbar(track_bar_h_min, window_name,
                      97, 360, get_track_bar_value)
    cv.createTrackbar(track_bar_h_max, window_name,
                      232, 360, get_track_bar_value)
    cv.createTrackbar(track_bar_s_min, window_name,
                      30, 100, get_track_bar_value)
    cv.createTrackbar(track_bar_s_max, window_name,
                      60, 100, get_track_bar_value)
    cv.createTrackbar(track_bar_v_min, window_name,
                      35, 100, get_track_bar_value)
    cv.createTrackbar(track_bar_v_max, window_name,
                      60, 100, get_track_bar_value)

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
        cv.imshow(window_name, composite_image)

        # 按下 Esc 键退出程序
        if cv.waitKey(1) & 0xFF == 27:
            break

    cv.destroyAllWindows()
    my_camera.stop_video_stream()
    my_robot.close()

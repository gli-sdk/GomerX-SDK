import cv2 as cv
import numpy as np
from gomerx import robot


if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_camera = my_robot.camera
    my_camera.start_video_stream(display=False)
    while True:
        img = my_camera.read_cv_image()
        if img is not None:
            break

                # 滑动条的回调函数，获取滑动条位置处的值
    def empty(a):
        h_min = cv.getTrackbarPos("Hue Min", "TrackBars")
        h_max = cv.getTrackbarPos("Hue Max", "TrackBars")
        s_min = cv.getTrackbarPos("Sat Min", "TrackBars")
        s_max = cv.getTrackbarPos("Sat Max", "TrackBars")
        v_min = cv.getTrackbarPos("Val Min", "TrackBars")
        v_max = cv.getTrackbarPos("Val Max", "TrackBars")
        # print(h_min, h_max, s_min, s_max, v_min, v_max)
        return h_min, h_max, s_min, s_max, v_min, v_max

    # 创建一个窗口，放置6个滑动条
    cv.namedWindow("TrackBars", 0)
    cv.resizeWindow('TrackBars', 900, 800)
    cv.createTrackbar("Hue Min", "TrackBars", 50, 179, empty)
    cv.createTrackbar("Hue Max", "TrackBars", 100, 179, empty)
    cv.createTrackbar("Sat Min", "TrackBars", 100, 255, empty)
    cv.createTrackbar("Sat Max", "TrackBars", 180, 255, empty)
    cv.createTrackbar("Val Min", "TrackBars", 50, 255, empty)
    cv.createTrackbar("Val Max", "TrackBars", 225, 255, empty)

    while True:
        img = my_camera.read_cv_image()
        imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        # 调用回调函数，获取滑动条的值
        h_min, h_max, s_min, s_max, v_min, v_max = empty(0)
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        # 获得指定颜色范围内的掩码
        mask = cv.inRange(imgHSV, lower, upper)

        # 单通道扩展为三通道
        mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)

        # 对原图图像进行按位与的操作，掩码区域保留
        # imgResult = cv.bitwise_and(img, img, mask=mask)
        # 对阈值处理后的图和原图进行拼接
        composite_image = np.hstack((img, mask))
        cv.imshow("TrackBars", composite_image)
        if cv.waitKey(1) & 0xFF == 27:
            break

        
   
    cv.destroyAllWindows()
    my_camera.stop_video_stream()
    my_robot.close()








path = 'test.jpg'


while True:
    img = cv.imread(path)
    imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    # 调用回调函数，获取滑动条的值
    h_min, h_max, s_min, s_max, v_min, v_max = empty(0)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    # 获得指定颜色范围内的掩码
    mask = cv.inRange(imgHSV, lower, upper)
    # 对原图图像进行按位与的操作，掩码区域保留
    imgResult = cv.bitwise_and(img, img, mask=mask)
    # 对阈值处理后的图和原图进行拼接
    composite_image = np.hstack((img, imgResult))

    cv.imshow("TrackBars", composite_image)

    if cv.waitKey(1) & 0xFF == 27:
        break

cv.destroyAllWindows()

from gomerx import robot
import cv2 as cv
import numpy as np

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_camera = my_robot.camera

    my_camera.start_video_stream(display=False)
    img = my_camera.read_cv_image()

    # 画一条直线,起点(50,70), 终点(70, 200)
    img = cv.line(img, (50, 70), (70, 200), color=(255, 0, 0), thickness=2)

    # 画一个矩形,左上角(130,50),右下角(180,150)
    img = cv.rectangle(img, (130, 50), (180, 150),
                       color=(0, 0, 255), thickness=1)

    # 画一个圆，圆心坐标(250, 150), 半径=30
    img = cv.circle(img, (250, 150), 30, color=(0, 255, 0), thickness=2)

    cv.imshow('img', img)
    if cv.waitKey(5000) == 27:
        cv.destroyAllWindows()
    my_camera.stop_video_stream()
    my_robot.close()

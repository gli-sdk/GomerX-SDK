from gomerx import robot
import cv2 as cv
import numpy as np
import time

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_camera = my_robot.camera
    my_camera.start_video_stream(display=False)

    print('按 ESC 键退出')

    while True:
        img = my_camera.read_cv_image()
        if img is not None:
            h, w = img.shape[0], img.shape[1]

            # 画一条直线
            x1, y1 = int(h/5), int(w/2)
            x2, y2 = int(h/5), int(w/4)
            img = cv.line(img, (x1, y1), (x2, y2),
                          color=(255, 0, 0), thickness=2)

            # 画一个矩形
            x1, y1 = int(h/4), int(w/2)
            x2, y2 = int(h/2), int(w/4)
            img = cv.rectangle(img, (x1, y1), (x2, y2),
                               color=(0, 0, 255), thickness=1)

            # 画一个圆
            x1, y1 = int(h/2)+100, int(w/2)-100
            r = int(w/12)
            img = cv.circle(img, (x1, y1), r, color=(0, 255, 0), thickness=2)

            cv.imshow('img', img)
            if cv.waitKey(10) == 27:
                cv.destroyAllWindows()
                break

    my_camera.stop_video_stream()
    my_robot.close()

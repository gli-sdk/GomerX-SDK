from gomerx import robot
import cv2 as cv
import numpy as np

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)

    n = 300
    img = np.ones((n, n, 3), np.uint8)*255
    img = cv.line(img, (50, 70), (70, 200), (255, 0, 0), 2)
    img = cv.rectangle(img, (130, 50), (180, 150), (0, 0, 255), 1)
    img = cv.circle(img, (250, 150), 30, (0, 255, 0), 2)

    cv.imshow('img', img)
    cv.waitKey()
    cv.destroyAllWindows()
    my_robot.close()

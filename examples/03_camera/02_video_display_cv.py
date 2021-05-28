import cv2 as cv
from gomerx import robot

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_camera = my_robot.camera
    my_camera.start_video_stream(display=False)
    while True:
        img = my_camera.read_cv_image()
        if img is not None:
            cv.imshow("img", img)
            if cv.waitKey(27) == 27:
                break

    my_camera.stop_video_stream()
    my_robot.close()

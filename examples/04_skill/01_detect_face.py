from gomerx import robot
import cv2 as cv
import time

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_camera = my_robot.camera
    my_skill = my_robot.skill
    my_camera.start_video_stream(display=False)
    while True:
        img = my_camera.read_cv_image()
        if img is None:
            continue
        result = my_skill.detect_face()
        if result:
            print("Found face")
            cv.putText(img, 'face', (0, 100), fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=3, color=(0, 255, 0), thickness=5)
        else:
            print("Not Found face")
            cv.putText(img, 'no face', (0, 100), fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=3, color=(0, 0, 255), thickness=5)
        cv.imshow('win', img)
        if cv.waitKey(20) == 27:
            break
    cv.destroyAllWindows()
    my_camera.stop_video_stream()
    my_robot.close()

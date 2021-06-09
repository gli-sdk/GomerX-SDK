from gomerx import robot
import cv2 as cv

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_skill = my_robot.skill
    my_camera = my_robot.camera

    my_camera.start_video_stream(display=False)
    while True:
        img = my_camera.read_cv_image()
        if img is None:
            print("未读取到图片")
        else:
            cv.imshow('img', img)
            key = cv.waitKey() 
            if key==ord('q'):
                break
            elif key==ord('s'):
                cv.imwrite('img.jpg')
                break

    my_camera.stop_video_stream()
    my_robot.close()

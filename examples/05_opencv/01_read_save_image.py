from gomerx import robot
import cv2 as cv

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_skill = my_robot.skill
    my_camera = my_robot.camera

    bool = my_camera.start_video_stream(display=False)
    if bool == True:
        print('视频流已打开')
        print('按下数字键 1，退出显示。\n按下数字键 2，保存图片。')
        while True:
            img = my_camera.read_cv_image()
            cv.imshow('img', img)
            key = cv.waitKey(50)
            if key == ord('1'):
                break
            elif key == ord('2'):
                cv.imwrite('img.jpg', img)
                break
    else:
        print('视频流未打开')

    my_camera.stop_video_stream()
    my_robot.close()

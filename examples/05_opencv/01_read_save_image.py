from gomerx import robot
import cv2 as cv

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_skill = my_robot.skill
    my_camera = my_robot.camera
    my_camera.start_video_stream(display=False)

    print('按下数字键 1, 退出显示。\n按下数字键 2, 保存图片。')
    image_num = 1
    while True:
        img = my_camera.read_cv_image()
        if img is not None:
            cv.imshow('img', img)
            key = cv.waitKey(1)
            if key == ord('1'):
                break
            elif key == ord('2'):
                image_name = 'img' + str(image_num) + '.jpg'
                cv.imwrite(image_name, img)
                image_num = image_num + 1

    my_camera.stop_video_stream()
    my_robot.close()

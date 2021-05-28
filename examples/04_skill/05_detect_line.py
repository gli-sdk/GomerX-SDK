from gomerx import robot
import cv2 as cv

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_camera = my_robot.camera
    my_skill = my_robot.skill
    my_camera.start_video_stream(display=False)

    # 设置蓝色的HSV值上下限
    hsv_low = (220, 20, 20)
    hsv_high = (260, 100, 100)

    while True:
        result, line = my_skill.detect_line(hsv_low, hsv_high)
        img = my_camera.read_cv_image()
        if img is None:
            continue
        if result:
            print("Found blue line at ", line)
            x0 = line[0]
            y0 = line[1]
            x1 = line[2]
            y1 = line[3]
            cv.line(img, (x0, y0), (x1, y1), (0, 255, 0), 2)
        else:
            print("Not Found blue line")

        cv.imshow('img', img)
        if cv.waitKey(50) == 27:
            break

    cv.destroyAllWindows()
    my_camera.stop_video_stream()
    my_robot.close()

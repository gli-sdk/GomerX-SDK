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
        result, rect = my_skill.detect_color_blob(hsv_low, hsv_high)
        img = my_camera.read_cv_image()
        if img is None:
            continue
        if result:
            print("Found blue at ", rect)
            x = rect[0]
            y = rect[1]
            w = rect[2]
            h = rect[3]
            top_left = (int(x - w / 2), int(y - h / 2))
            right_bottom = (int(x + w / 2), int(y + h / 2))
            cv.rectangle(img, top_left, right_bottom, (0, 255, 0), 2)
        else:
            print("Not Found blue")

        cv.imshow('img', img)
        if cv.waitKey(50) == 27:
            break

    cv.destroyAllWindows()
    my_camera.stop_video_stream()
    my_robot.close()

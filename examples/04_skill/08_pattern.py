from gomerx import robot
import cv2 as cv
import time
if __name__ == '__main__':
    robot_name = 'GomerX_SkOhHU'
    my_robot = robot.Robot(robot_name)
    my_camera = my_robot.camera
    my_skill = my_robot.skill
    my_camera.start_video_stream(display=False)

    i = 0
    while cv.waitKey(10) != 27:
        img = my_camera.read_cv_image()
        if img is None:
            continue
        cv.imshow('img', img)
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                   'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        pattern_id = letters[i % len(letters)]
        i += 1
        t1 = time.time()
        result = my_skill.detect_pattern(id=pattern_id)
        print('detect_pattern: {}s'.format(time.time() - t1))

        if result:
            # 如果有结果
            i -= 1
            print("found %s" % pattern_id)
            cv.putText(img, text=pattern_id, org=(
                0, 100), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=3, color=(0, 255, 0), thickness=5)
            cv.imshow('img', img)
            my_skill.move_to_pattern(pattern_id, x=0, y=12)
    cv.destroyAllWindows()
    my_robot.camera.stop_video_stream()
    my_robot.close()

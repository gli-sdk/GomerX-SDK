from gomerx import robot
import cv2 as cv
import numpy as np

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_camera = my_robot.camera

    bool = my_camera.start_video_stream(display=False)
    if bool == True:
        print('视频流已打开')
        print('按 ESC 键退出')
        while True:
            img = my_camera.read_cv_image()
            h,w = img.shape[0], img.shape[1]
            print(h,w)
            # 画一条直线
            x1,y1 = int(h/5), int(w/2)
            x2,y2 = int(h/5), int(w/4)
            img = cv.line(img, (x1, y1), (x2, y2), color=(255, 0, 0), thickness=2)

            # 画一个矩形
            x1,y1 = int(h/4), int(w/2)
            x2,y2 = int(h/2), int(w/4)
            img = cv.rectangle(img, (x1, y1), (x2, y2),
                            color=(0, 0, 255), thickness=1)
            
            # 画一个圆
            x1,y1 = int(h/2), int(w/2)
            r = int(w/6)
            img = cv.circle(img, (x1, y1), r, color=(0, 255, 0), thickness=2)

            cv.imshow('img', img)
            if cv.waitKey(10) == 27:
                print('1')
                cv.destroyAllWindows()
                break
    else:
        print('视频流打开失败')
        
    my_camera.stop_video_stream()
    my_robot.close()

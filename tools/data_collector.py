import cv2 as cv
import numpy as np
import os
import copy
import sys
from gomerx import robot

WINDOW_NAME = "Data Collector"
CLASSES_DIR = ["sample1", "sample2", "sample3"]
TMP_FILE_DIR = "/tmp/"
CURRENT_WORK_DIR = os.getcwd()  # 获得当前目录


def init_window():
    cv.namedWindow(WINDOW_NAME, cv.WINDOW_GUI_NORMAL)
    cv.resizeWindow(WINDOW_NAME, 1000, 800)

    if os.path.isdir(CURRENT_WORK_DIR + TMP_FILE_DIR) is False:
        os.mkdir(CURRENT_WORK_DIR + TMP_FILE_DIR)

    for tmp_dir in CLASSES_DIR:
        if os.path.isdir(CURRENT_WORK_DIR + TMP_FILE_DIR + tmp_dir) is False:
            os.mkdir(CURRENT_WORK_DIR + TMP_FILE_DIR + tmp_dir)


def draw_text(image, classes_index, picture_index):
    # 给图片添加文字
    line1_text = "Press 'S' to take picture and 'Q' to quit"
    line2_text = "Take Picture for %s ( %d/9 )" % (
        CLASSES_DIR[classes_index], picture_index)

    cv.putText(image, line1_text, (30, 40), cv.FONT_HERSHEY_SIMPLEX,
               1, (0, 255, 0), 2, 8)
    cv.putText(image, line2_text, (30, 70), cv.FONT_HERSHEY_SIMPLEX,
               1, (0, 255, 0), 2, 8)
    return image


def draw_rectangle(text_image):
    # 画一个矩形，并返回矩形的坐标
    row, col, channel = text_image.shape
    longe_edge = max(row, col)
    short_edge = min(row, col)
    square_edge = int(short_edge/2)
    core_index = (int(longe_edge/2), int(short_edge/2))
    top_left_coordinate = (
        core_index[0]-square_edge, core_index[1]-square_edge)
    bottom_right_coordinate = (
        core_index[0]+square_edge, core_index[1]+square_edge)
    show_image = cv.rectangle(text_image, top_left_coordinate,
                              bottom_right_coordinate, (0, 0, 255), 3)
    rectangle_coordinate = (top_left_coordinate, bottom_right_coordinate)

    return show_image, rectangle_coordinate


def crop_and_resize_rectangle(image, coordinate):
    square_image = image[coordinate[0][1]:coordinate[1][1],
                         coordinate[0][0]:coordinate[1][0]]
    return cv.resize(square_image, (224, 224))


if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_camera = my_robot.camera
    my_camera.start_video_stream(display=False)

    # 确保得到视频流之后再显示窗口显示图片
    while True:
        img = my_camera.read_cv_image()
        if img is not None:
            break

    # 初始化窗口
    init_window()
    # 实际的图片个数 = max_picture_num - picture_num
    current_picture_num = 0
    max_picture_num = 9

    # 类别的个数
    current_classes_num = 0
    max_classes_num = 3

    while True:
        frame = my_camera.read_cv_image()
        raw_image_copy = copy.deepcopy(frame)
        # 添加方框
        show_image, rectangle_coordinate = draw_rectangle(frame)
        # 添加文字
        text_image = draw_text(
            show_image, current_classes_num, current_picture_num)
        # 裁剪图片，保存为一个正方形
        save_image = crop_and_resize_rectangle(
            raw_image_copy, rectangle_coordinate)
        # 展示图片
        cv.imshow(WINDOW_NAME, text_image)

        key = cv.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('s'):
            save_path = CURRENT_WORK_DIR + TMP_FILE_DIR + CLASSES_DIR[current_classes_num] + "/" + \
                str(current_picture_num+1) + '.png'
            cv.imencode('.png', save_image)[1].tofile(save_path)

            current_picture_num += 1
            if current_picture_num == max_picture_num:
                current_classes_num += 1
                current_picture_num = 0

        if current_classes_num == max_classes_num:
            break

    cv.destroyAllWindows()

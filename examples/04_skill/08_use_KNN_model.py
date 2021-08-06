from tensorflow.keras.applications.mobilenet import MobileNet
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.applications.mobilenet import preprocess_input
import cv2 as cv
import os
import numpy as np
from gomerx import robot

WINDOW_NAME = "Machine Learning"
SAMPLE_NUM = 3
IMAGE_NUM = 9
SAMPLE_DIR = 'sample'
TMP_FILE_DIR = "/tmp/"
CURRENT_WORK_DIR = os.getcwd()


def get_videostream_image_feature(image_path, model):
    img = cv.resize(image_path, (224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    feature = model.predict(x)
    return feature[0][0][0]


def KNN_classify(input, dataSet, label, k=10):
    data_size = dataSet.shape[0]
    # 计算欧式距离
    diff = np.tile(input, (data_size, 1)) - dataSet
    sqdiff = diff ** 2
    square_dist = np.sum(sqdiff, axis=1)  # 行向量分别相加，从而得到新的一个行向量
    dist = square_dist ** 0.5

    # 对距离进行排序
    sorted_dist_index = np.argsort(dist)  # argsort()根据元素的值从大到小对元素进行排序，返回下标

    # 构建字典，为后面得到比例做准备
    class_count = {1: 0, 2: 0, 3: 0}
    for i in range(k):
        voteLabel = label[sorted_dist_index[i]]
        # 对选取的K个样本所属的类别个数进行统计
        class_count[voteLabel] = class_count.get(voteLabel, 0) + 1

    return class_count


def draw_rectangle(raw_image):
    # 画一个矩形，并返回矩形的坐标
    row, col, channel = raw_image.shape
    longe_edge = max(row, col)
    short_edge = min(row, col)
    square_edge = int(short_edge/2)
    core_index = (int(longe_edge/2), int(short_edge/2))
    top_left_coordinate = (
        core_index[0]-square_edge, core_index[1]-square_edge)
    down_right_coordinate = (
        core_index[0]+square_edge, core_index[1]+square_edge)
    rectangle_image = cv.rectangle(raw_image, top_left_coordinate,
                                   down_right_coordinate, (0, 0, 255), 3)

    return rectangle_image


def draw_category_ration_text(image, classes_dict):
    # 计算概率
    confidence_A = classes_dict.get(1)/10
    confidence_B = classes_dict.get(2)/10
    confidence_C = classes_dict.get(3)/10
    # 给图片添加文字
    line1_text = " sample1 : %3d %% " % (confidence_A*100)
    line2_text = " sample2 : %3d %% " % (confidence_B*100)
    line3_text = " sample3 : %3d %% " % (confidence_C*100)
    rectangle_image = draw_rectangle(image)
    cv.putText(rectangle_image, line1_text, (30, 40), cv.FONT_HERSHEY_SIMPLEX,
               1, (0, 255, 0), 2, 8)
    cv.putText(rectangle_image, line2_text, (30, 70), cv.FONT_HERSHEY_SIMPLEX,
               1, (0, 255, 0), 2, 8)
    cv.putText(rectangle_image, line3_text, (30, 100), cv.FONT_HERSHEY_SIMPLEX,
               1, (0, 255, 0), 2, 8)

    return rectangle_image


if __name__ == '__main__':
    # 指定模型到某一层截至，只获得指定层的输出
    base_model = MobileNet(weights='imagenet')
    model = Model(inputs=base_model.input,
                  outputs=base_model.get_layer('dropout').output)

    # 连接机器人
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_camera = my_robot.camera
    my_camera.start_video_stream(display=False)

    # 加载train_model产生的数据文件
    model_data = np.load(CURRENT_WORK_DIR+TMP_FILE_DIR + 'model_data.npy')
    features = model_data[:, 0:1024]
    labels = model_data[:, 1024]
    print('加载模型数据完毕')

    while True:
        frame = my_camera.read_cv_image()
        if frame is not None:
            print("分类程序开始，放置不同类别的物品")
            image_feature = get_videostream_image_feature(frame, model)
            classes_dict = KNN_classify(image_feature, features, labels, k=10)
            ration_image = draw_category_ration_text(frame, classes_dict)
            if classes_dict[2] >= 9:
                # 如果是第二类，则动一动机械臂
                # 如果是第一类，则开闭爪子
                my_gripper = my_robot.gripper
                my_gripper.close()
                my_gripper.open()
            elif classes_dict[3] >= 9:
                my_arm = my_robot.arm
                my_arm.move_to(12, 10)
                my_arm.move_to(12, 15)
            else:
                continue

            if cv.waitKey(1) == 27:
                break

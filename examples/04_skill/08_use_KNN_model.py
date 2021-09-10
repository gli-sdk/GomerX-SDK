# 导入我们所需要的模块
from tensorflow.keras.applications.mobilenet import MobileNet
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.applications.mobilenet import preprocess_input
import cv2 as cv
import os
import numpy as np
from gomerx import robot

# 定义一些后面会用到的常量
WINDOW_NAME = "Machine Learning"
SAMPLE_NUM = 3
IMAGE_NUM = 9
SAMPLE_DIR = 'sample'
TMP_FILE_DIR = "/tmp/"
CURRENT_WORK_DIR = os.getcwd()


def get_videostream_image_feature(image_path, model):
    # 定义函数，处理得到的视频流。能够用于分类模型
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
    # 行向量分别相加，从而得到新的一个行向量
    square_dist = np.sum(sqdiff, axis=1)
    dist = square_dist ** 0.5

    # 对距离进行排序
    sorted_dist_index = np.argsort(dist)

    # 构建字典，为后面得到比例做准备
    class_count = {1: 0, 2: 0, 3: 0}
    for i in range(k):
        voteLabel = label[sorted_dist_index[i]]
        # 对选取的K个样本所属的类别个数进行统计
        class_count[voteLabel] = class_count.get(voteLabel, 0) + 1

    return class_count


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
    print("分类程序开始，放置不同类别的物品")
    # 开始控制机器人
    while True:
        frame = my_camera.read_cv_image()
        if frame is not None:
            image_feature = get_videostream_image_feature(frame, model)
            classes_dict = KNN_classify(image_feature, features, labels, k=10)
            if classes_dict[2] >= 9:
                # 如果是第二类，则开闭爪子
                my_gripper = my_robot.gripper
                my_gripper.close()
                my_gripper.open()
            elif classes_dict[3] >= 9:
                # 如果是第三类，则动一动机械臂
                my_arm = my_robot.arm
                my_arm.move_to(12, 10)
                my_arm.move_to(12, 15)
            else:
                # 如果是其他情况则保持不动
                continue

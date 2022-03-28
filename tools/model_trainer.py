from tensorflow.keras.applications.mobilenet import MobileNet
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.applications.mobilenet import preprocess_input
import os
import numpy as np
import time

WINDOW_NAME = "Machine Learning"
SAMPLE_NUM = 3
IMAGE_NUM = 9
SAMPLE_DIR = 'sample'
TMP_FILE_DIR = "/tmp/"
CURRENT_WORK_DIR = os.getcwd()


def get_image_feature(image_path, model):
    img = image.load_img(image_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    feature = model.predict(x)
    return feature[0][0][0]


def preprocess_dataset(sample_num, image_num, SAMPLE_DIR):
    # 取出特征和标签
    features = []
    labels = []
    for i in range(1, sample_num+1):
        for j in range(1, image_num+1):
            img = CURRENT_WORK_DIR + TMP_FILE_DIR + \
                SAMPLE_DIR + str(i) + '/'+str(j)+'.png'
            feature = get_image_feature(img, model)
            features.append(feature)
            labels.append(i)
    return np.array(features), labels


def knn_classify(input, data_set, label, k=10):
    data_size = data_set.shape[0]
    # 计算欧式距离
    diff = np.tile(input, (data_size, 1)) - data_set
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


if __name__ == '__main__':

    print('\n\n开始构建模型\n')
    # 加载 mobilenet模型
    base_model = MobileNet(weights='imagenet')
    # 指定模型到某一层截至，只获得指定层的输出
    model = Model(inputs=base_model.input,
                  outputs=base_model.get_layer('dropout').output)
    print('\n\n模型构建完成\n')

    # 整理得到数据和标签
    print('开始提取特征\n')

    start = time.time()
    features, labels = preprocess_dataset(SAMPLE_NUM, IMAGE_NUM, SAMPLE_DIR)
    labels = np.array(labels).reshape(27, 1)
    model_data = np.hstack((features, labels))
    np.save(CURRENT_WORK_DIR + TMP_FILE_DIR + 'model_data', model_data)
    end = time.time()
    print('特征提取完毕!')
    print('耗时: %.4f s' % (end-start))

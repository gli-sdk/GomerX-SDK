import time
from gomerx import robot
from gomerx.skill import LINE_CROSS, LINE_END
from tensorflow.keras.applications.mobilenet import MobileNet
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.applications.mobilenet import preprocess_input
import cv2 as cv
import os
import numpy as np


LINE_COLOR_LOW = (16, 21, 19)
LINE_COLOR_HIGH = (66, 100, 100)
YELLOW_LOW = (24, 45, 0)
YELLOW_HIGH = (82, 100, 100)
PURPLE_LOW = (270, 48, 0)
PURPLE_HIGH = (360, 100, 100)
PATIENT = 'P'
SAMPLE = 'S'
PHYSICIAN = 'P'
ROOM = 'R'
MEDICINE = 'M'
MEDICINE_PLACE = 'W'
BUTTON = 'B'
PALM = 1
FIST = 2
MEN_PATIENT = '1'
WOMEN_PATIENT = '2'
HOUSEHOLD_WASTE = '1'
MEDICAL_WASTE = '2'
HOUSEHOLD_TRASH = '1'
MEDICAL_TRASH = '2'
WINDOW_NAME = "Machine Learning"
SAMPLE_NUM = 3
IMAGE_NUM = 9
SAMPLE_DIR = 'sample'
TMP_FILE_DIR = "/tmp/"
CURRENT_WORK_DIR = os.getcwd()


# 抓取
def grab(robot: robot.Robot):
    robot.arm.move_to(y=14, z=5)
    robot.chassis.move(y=2)
    robot.gripper.close()
    robot.servo.reset()


# 放置
def put_down(robot: robot.Robot):
    robot.arm.move_to(y=14, z=5)
    robot.gripper.open()
    robot.chassis.move(y=-3)
    robot.servo.reset()




def clean_garbage(robot: robot.Robot):
    print("清理垃圾......")
    rubbish_id = ''
    rubbish_bin_id = ''
    robot.arm.move_to(y=12, z=15)
    robot.gripper.open()
    robot.chassis.move_forward(y=10)
    # drive_line(robot, line_stop=LINE_CROSS)
    if robot.skill.detect_line(hsv_low=LINE_COLOR_LOW, hsv_high=LINE_COLOR_HIGH):
        print("识别到线段")
        robot.skill.move_along_line(stop=LINE_CROSS)
    else:
        print("没有识别到线段")
        robot.chassis.move_to_left(x=25)
        robot.chassis.advance(60)
    # 区分垃圾
    if robot.skill.detect_pattern(id=HOUSEHOLD_WASTE, timeout=1):
        print("发现生活垃圾")
        rubbish_id = HOUSEHOLD_WASTE
        rubbish_bin_id = HOUSEHOLD_TRASH
    elif robot.skill.detect_pattern(id=MEDICAL_WASTE, timeout=1):
        print("发现医疗垃圾")
        rubbish_id = MEDICAL_WASTE
        rubbish_bin_id = MEDICAL_TRASH
    else:
        rubbish_id = ''
        print("未发现垃圾")
    # 抓取垃圾
    if rubbish_id != '':
        robot.skill.move_to_pattern(id=rubbish_id, y=15)
        grab(robot)
        robot.arm.move_to(y=12, z=15)
        robot.chassis.rotate(a=90)
        robot.chassis.retreat(y=10)
        # 放置到对应垃圾桶中
        if robot.skill.detect_pattern(id=rubbish_bin_id):
            print("找到垃圾桶")
            robot.skill.move_to_pattern(id=rubbish_bin_id, y=14)
            robot.chassis.advance(y=4)
            robot.gripper.open()
            robot.chassis.retreat(y=15)
            robot.servo.reset()
            if rubbish_bin_id == HOUSEHOLD_TRASH:
                robot.chassis.move_right(x=30)
            else:
                robot.chassis.move_right(x=50)
        else:
            print("未找到垃圾桶")
            robot.gripper.open()
            robot.servo.reset()
            robot.chassis.move_right(x=45)
    else:
        robot.chassis.rotate(a=90)
        robot.chassis.move_right(x=35)


def guide_patient(robot: robot.Robot):
    print("获取病人信息")
    # 根据二维码中的病人信息抓取病人
    ret, patient = robot.skill.detect_qrcode()
    robot.chassis.move(x=5)
    if robot.skill.detect_pattern(id=PATIENT):
        print("找到病人")
        robot.skill.move_to_pattern(id=PATIENT, y=16)
        grab(robot)
        robot.chassis.move_backward(y=10)
        robot.chassis.rotate(a=-90)
        if robot.skill.detect_line(hsv_low=LINE_COLOR_LOW, hsv_high=LINE_COLOR_HIGH):
            robot.skill.move_along_line(stop=LINE_END)
        else:
            robot.chassis.move_forward(y=150)
        robot.chassis.rotate(a=-90)
        if robot.skill.detect_pattern(id=ROOM):
            print("到达诊室")
            robot.skill.move_to_pattern(id=ROOM, y=15)
        else:
            robot.chassis.move_forward(y=5)
        # 根据二维码的病人信息放置到对应诊室
        if ret:
            if patient == WOMEN_PATIENT:
                print("送到2号诊室")
                robot.chassis.move_left(x=20)
            else:
                print("送到1号诊室")
                robot.chassis.move_right(x=20)
        else:
            robot.chassis.move_right(x=20)
        if robot.skill.detect_pattern(id=PHYSICIAN):
            robot.skill.move_to_pattern(id=PHYSICIAN, y=35)
        else:
            robot.chassis.move_forward(y=10)
        put_down(robot)
        # 离开诊室，前往样本室
        robot.chassis.move_backward(y=10)
        if ret:
            if patient == WOMEN_PATIENT:
                robot.chassis.move_left(x=10)
            else:
                robot.chassis.move_left(x=50)
        else:
            robot.chassis.move_left(x=50)
        robot.chassis.rotate(a=180)
        robot.chassis.move_forward(y=10)
    else:
        print("未找到病人，前往样本室")
        robot.chassis.move_backward(y=10)
        robot.chassis.rotate(a=-90)
        robot.chassis.move_forward(y=90)
        robot.chassis.rotate(a=90)


def deliver_sample(robot: robot.Robot):
    print("送样检查")
    sample_color = [(0, 0, 0), (360, 100, 100)]
    # 识别样本的颜色
    ret, sample_ord = robot.skill.detect_color_blob(
        hsv_low=YELLOW_LOW, hsv_high=YELLOW_HIGH)
    print(ret, sample_ord)
    if ret:
        sample_color = [YELLOW_LOW, YELLOW_HIGH]
    else:
        sample_color = [PURPLE_LOW, PURPLE_HIGH]
    # 抓取样本
    if robot.skill.detect_pattern(id=SAMPLE):
        print("发现样本")
        robot.skill.move_to_pattern(id=SAMPLE, y=16)
        grab(robot)
        robot.chassis.move_backward(y=14)
        robot.chassis.move_right(x=38)
        # 前往消毒室
        robot.chassis.move(a=180)
        if robot.skill.detect_line(hsv_low=LINE_COLOR_LOW, hsv_high=LINE_COLOR_HIGH):
            robot.skill.move_along_line(stop=LINE_END)
        else:
            robot.chassis.move_forward(y=35)
        ret, turntable_ord = robot.skill.detect_color_blob(
            sample_color[0], sample_color[1], timeout=10)
        x, y, w, h = turntable_ord
        if ret:
            while w < 700:
                time.sleep(0.1)
                ret, sample_ord = robot.skill.detect_color_blob(
                    sample_color[0], sample_color[1])
        # 放到消毒转盘上的对应区域
        robot.arm.move_to(y=13, z=10)
        robot.chassis.move_forward(y=5)
        robot.gripper.open()
        robot.chassis.move_backward(y=2)
        robot.servo.reset()
        robot.chassis.move_backward(y=15)
        # 离开消毒室，前往药房
        robot.chassis.rotate(a=90)
        robot.chassis.move_right(x=5)
        if robot.skill.detect_line(hsv_low=LINE_COLOR_LOW, hsv_high=LINE_COLOR_HIGH):
            robot.skill.move_along_line(stop=LINE_END)
        else:
            robot.chassis.move_backward(y=85)
        robot.chassis.rotate(a=90)
    else:
        # 直接前往药房
        print("没有样本")
        robot.chassis.move_left(x=40)


def move_to_ward(robot: robot.Robot):
    print("前往病房")
    robot.chassis.rotate(a=90)
    if robot.skill.detect_line(hsv_low=LINE_COLOR_LOW, hsv_high=LINE_COLOR_HIGH):
        print("自动前往病房")
        robot.skill.move_along_line(stop=LINE_END)
    else:
        print("机动前往病房")
        robot.chassis.move_forward(y=150)
    robot.chassis.rotate(a=90)
    print("岔路口拐弯，进入病房")
    if robot.skill.detect_line(hsv_low=LINE_COLOR_LOW, hsv_high=LINE_COLOR_HIGH):
        robot.skill.move_along_line(stop=LINE_END)
    else:
        robot.chassis.move_forward(y=55)


def deliver_medicine(robot: robot.Robot):
    print("进入药房")
    if robot.skill.detect_pattern(id=MEDICINE):
        print("发现药品")
        robot.skill.move_to_pattern(id=MEDICINE, y=16)
        robot.arm.move_to(y=14, z=8)
        robot.chassis.move_forward(y=2)
        robot.gripper.close()
        robot.arm.move_to(y=14, z=10)
        robot.chassis.move_backward(y=5)
        robot.servo.reset()
        robot.chassis.move_backward(y=10)
        move_to_ward(robot)
        robot.chassis.rotate(a=90)
        if robot.skill.detect_pattern(id=MEDICINE_PLACE):
            print("发现药品放置区")
            robot.skill.move_to_pattern(id=MEDICINE_PLACE, y=18)
        else:
            print("未发现放置区标志")
            robot.chassis.move_forward(y=5)
        put_down(robot)
        robot.chassis.rotate(a=180)
    else:
        print("没有药品")
        move_to_ward(robot)
        robot.chassis.rotate(a=-90)


def knock_on(robot: robot.Robot):
    robot.arm.move_to(y=12, z=10)
    time.sleep(0.1)
    robot.servo.reset()


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


gesture_id = 0


def machine_learning(robot: robot.Robot):
    # 指定模型到某一层截至，只获得指定层的输出
    base_model = MobileNet(weights='imagenet')
    model = Model(inputs=base_model.input,
                  outputs=base_model.get_layer('dropout').output)
    # 连接机器人
    robot.camera.start_video_stream(display=False)
    # 加载train_model产生的数据文件
    model_data = np.load(CURRENT_WORK_DIR+TMP_FILE_DIR + 'model_data.npy')
    features = model_data[:, 0:1024]
    labels = model_data[:, 1024]
    print('加载模型数据完毕')
    print("分类程序开始，放置不同类别的物品")
    global gesture_id
    # 开始控制机器人
    while True:
        frame = robot.camera.read_cv_image()
        if frame is not None:
            image_feature = get_videostream_image_feature(frame, model)
            classes_dict = KNN_classify(image_feature, features, labels, k=10)
            if classes_dict[1] >= 9:
                gesture_id = PALM
                break
            elif classes_dict[2] >= 9:
                gesture_id = FIST
                break
            else:
                gesture_id = 0
                break
    robot.camera.stop_video_stream()


def assist_patient(robot: robot.Robot):
    machine_learning(robot)
    if gesture_id != 0:
        robot.chassis.move(x=-20)
        if robot.skill.detect_pattern(id=BUTTON):
            robot.skill.move_to_pattern(id=BUTTON, y=14)
        robot.chassis.move(y=5)
        robot.gripper.close()
        if gesture_id == PALM:
            knock_on(robot)
        else:
            knock_number = 0
            while knock_number < 2:
                knock_on(robot)
                knock_number = knock_number+1
        robot.chassis.move(y=-10)
    else:
        print("no patient assistance")
    robot.chassis.move(a=-90)


def return_terminus(robot: robot.Robot):
    print("返回起点")
    if robot.skill.detect_line(LINE_COLOR_LOW, LINE_COLOR_HIGH):
        robot.skill.move_along_line(stop=LINE_CROSS)
    else:
        robot.chassis.move_forward(y=40)
    robot.chassis.move_forward(y=20)
    robot.chassis.move_right(x=5)
    robot.chassis.rotate(a=-90)
    robot.chassis.move_backward(y=20)


if __name__ == '__main__':
    name = 'GomerX_6e09ba'
    gomerx = robot.Robot(name)
    clean_garbage(gomerx)
    guide_patient(gomerx)
    deliver_sample(gomerx)
    deliver_medicine(gomerx)
    assist_patient(gomerx)
    return_terminus(gomerx)

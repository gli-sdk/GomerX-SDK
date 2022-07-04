# 导入库文件
from gomerx import robot
from gomerx import led
import time


def robot_init(my_robot):  # 初始化状态
    my_robot.chassis.move(x=0, y=0, a=0, wait_for_complete=True)
    my_robot.arm.move_to(12, 15)
    my_robot.gripper.open()
    my_robot.servo.move_to(0, 150)
    my_robot.servo.move_to(1, 50)


def robot_capture(pattern_id, my_robot):  # 进货区抓取货物ABC
    if pattern_id == 'A':
        my_robot.chassis.move(x=-22)
    elif pattern_id == 'C':
        my_robot.chassis.move(x=22)
    result = my_robot.skill.detect_pattern(id=pattern_id)
    if result:
        my_robot.skill.move_to_pattern(pattern_id, x=0, y=15)
        my_robot.arm.move_to(13, 2)
        my_robot.chassis.move(y=2)
        my_robot.gripper.close()
        my_robot.servo.move_to(0, 150)
        my_robot.servo.move_to(1, 70)
        my_robot.chassis.move(y=-2)
    if pattern_id == 'A':
        my_robot.chassis.move(x=22)
    elif pattern_id == 'C':
        my_robot.chassis.move(x=-22)


def robot_move(pattern_id, my_robot):  # 移动到货架
    my_robot.chassis.move(a=180)
    if pattern_id == '1':  # 1号货架
        my_robot.chassis.move(y=15)
    elif pattern_id == '2':  # 2号货架
        my_robot.chassis.move(y=60)
    else:  # 3号货架
        my_robot.chassis.move(y=110)
    my_robot.chassis.move(a=-90)
    my_robot.chassis.move(y=10)


def robot_goods(pattern_id, my_robot):  # 放置货物到货架
    result = my_robot.skill.detect_pattern(id=pattern_id, timeout=5)
    if result:
        my_robot.skill.move_to_pattern(pattern_id, x=0, y=20)
        my_robot.arm.move_to(13, 2)
        my_robot.chassis.move(y=2)
        my_robot.gripper.open()
        my_robot.chassis.move(y=-10)
        my_robot.servo.move_to(0, 150)
        my_robot.servo.move_to(1, 70)


def robot_return(pattern_id, my_robot):  # 货架返回进货区
    my_robot.chassis.move(y=-10)
    my_robot.chassis.move(a=-90)
    if pattern_id == '2':
        my_robot.chassis.move(y=60)
    elif pattern_id == '3':
        my_robot.chassis.move(y=100)


def robot_capture1(pattern_id, my_robot):  # 从货架抓取货物
    my_robot.chassis.move(y=-10)
    my_robot.chassis.move(a=90)
    if pattern_id == 'A':
        my_robot.chassis.move(y=80)
        my_robot.chassis.move(a=90)
    elif pattern_id == 'B':
        my_robot.chassis.move(y=30)
        my_robot.chassis.move(a=90)
    else:
        my_robot.chassis.move(a=180)
    result = my_robot.skill.detect_pattern(id=pattern_id)
    if result:
        my_robot.skill.move_to_pattern(pattern_id, x=0, y=15)
        my_robot.arm.move_to(13, 2)
        my_robot.chassis.move(y=2)
        my_robot.gripper.close()
        my_robot.servo.move_to(0, 150)
        my_robot.servo.move_to(1, 70)
        my_robot.chassis.move(y=-30)
        my_robot.chassis.move(a=90)
        if pattern_id == 'A':
            my_robot.chassis.move(y=100)
        elif pattern_id == 'B':
            my_robot.chassis.move(y=60)


def robot_task(pattern_id, my_robot):  # 显示屏任务
    my_robot.chassis.move(a=180)
    my_robot.chassis.move(x=15)
    my_robot.chassis.move(y=15)
    result = my_robot.skill.detect_pattern(id=pattern_id)
    if result:
        my_robot.skill.move_to_pattern(pattern_id, x=0, y=20)
        if pattern_id == '1':
            robot_capture1(pattern_id='A', my_robot=my_robot)
        elif pattern_id == '2':
            robot_capture1(pattern_id='B', my_robot=my_robot)
        else:
            robot_capture1(pattern_id='C', my_robot=my_robot)


def robot_shipments(pattern_id, my_robot):  # 配货区
    result = my_robot.skill.detect_pattern(id=pattern_id)
    if result:
        my_robot.skill.move_to_pattern(pattern_id, x=0, y=20)
        my_robot.arm.move_to(18, 16)
        my_robot.chassis.move(y=2)
        my_robot.gripper.open()


def robot_finish(my_robot):  # 返回终点
    my_robot.chassis.move(x=-40)
    my_robot.chassis.move(y=20)
    my_robot.servo.move_to(0, 150)
    my_robot.gripper.close()


if __name__ == '__main__':
    # robot_name = input('Please input robot name: ')
    robot_name = 'GomerX_kMi774'
    my_robot = robot.Robot(robot_name)
    my_camera = my_robot.camera

    my_robot.camera.start_video_stream(display=True)  # 打开摄像头
    robot_init(my_robot=my_robot)
    my_robot.chassis.move(y=40)  # 出发
    my_robot.chassis.move(a=-90)
    my_robot.chassis.move(y=60)

    robot_capture(pattern_id='A', my_robot=my_robot)  # 抓取A
    robot_move(pattern_id='1', my_robot=my_robot)  # 至货架1的路线
    robot_goods(pattern_id='1', my_robot=my_robot)  # 货物A放置货架1
    robot_return(pattern_id='1', my_robot=my_robot)  # 返回出货区
    robot_capture(pattern_id='B', my_robot=my_robot)  # 抓取B
    robot_move(pattern_id='2', my_robot=my_robot)  # 至货架2的路线
    robot_goods(pattern_id='2', my_robot=my_robot)  # 货物B放置货架2
    robot_return(pattern_id='2', my_robot=my_robot)  # 返回出货区
    robot_capture(pattern_id='C', my_robot=my_robot)  # 抓取C
    robot_move(pattern_id='3', my_robot=my_robot)  # 至货架3的路线
    robot_goods(pattern_id='3', my_robot=my_robot)  # 货物C放置货架3
    robot_task(pattern_id='1',  my_robot=my_robot)  # 识别显示屏数字1的任务（2、3可自行修改）
    robot_shipments(pattern_id='B', my_robot=my_robot)  # 配货区任务
    robot_finish(my_robot=my_robot)  # 完成任务，返回终点
    my_robot.close()

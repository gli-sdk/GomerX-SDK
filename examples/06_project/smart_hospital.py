import time
from gomerx import robot
from gomerx.skill import LINE_CROSS, LINE_END


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


# 巡线
def drive_line(robot: robot.Robot, line_stop=LINE_END):
    if robot.skill.detect_line(LINE_COLOR_LOW, LINE_COLOR_HIGH):
        robot.skill.move_along_line(stop=line_stop)


# 移动到某处
def move_to_position(robot: robot.Robot, sign: str = 'A', distance: int = 16):
    if robot.skill.detect_pattern(id=sign):
        robot.skill.move_to_pattern(id=sign, y=distance)


def clean_garbage(robot: robot.Robot):
    waste_id = ''
    trash_id = ''
    robot.arm.move_to(y=12, z=15)
    robot.gripper.open()
    robot.chassis.move(y=10)
    drive_line(robot, line_stop=LINE_CROSS)
    # 区分垃圾
    if robot.skill.detect_pattern(id=HOUSEHOLD_WASTE, timeout=1):
        waste_id = HOUSEHOLD_WASTE
        trash_id = HOUSEHOLD_TRASH
    elif robot.skill.detect_pattern(id=MEDICAL_WASTE, timeout=1):
        waste_id = MEDICAL_WASTE
        trash_id = MEDICAL_TRASH
    else:
        exit()
    # 抓取垃圾
    robot.skill.move_to_pattern(id=waste_id, y=15)
    grab(robot)
    robot.arm.move_to(y=12, z=15)
    robot.chassis.move(a=90)
    robot.chassis.move(y=-10)
    # 放置到对应垃圾桶中
    move_to_position(robot, sign=trash_id, distance=14)
    robot.chassis.move(y=4)
    robot.gripper.open()
    robot.chassis.move(y=-15)
    robot.servo.reset()
    if trash_id == HOUSEHOLD_TRASH:
        robot.chassis.move(x=30)
    else:
        robot.chassis.move(x=50)


def guide_patient(robot: robot.Robot):
    # 根据二维码中的病人信息抓取病人
    qrdoce_result = robot.skill.detect_qrcode()
    robot.chassis.move(x=5)
    move_to_position(robot, sign=PATIENT)
    grab(robot)
    robot.chassis.move(y=-10)
    robot.chassis.move(a=-90)
    drive_line(robot)
    robot.chassis.move(a=-90)
    move_to_position(robot, sign=ROOM, distance=15)
    # 根据二维码的病人信息放置到对应诊室
    if qrdoce_result[0]:
        if qrdoce_result[1] == WOMEN_PATIENT:
            robot.chassis.move(x=-20)
    robot.chassis.move(x=20)
    move_to_position(robot, sign=PHYSICIAN, distance=35)
    put_down(robot)
    # 离开诊室，前往样本室
    robot.chassis.move(y=-10)
    if qrdoce_result[0]:
        if qrdoce_result[1] == WOMEN_PATIENT:
            robot.chassis.move(x=-10)
    robot.chassis.move(x=-50)
    robot.chassis.move(a=180)
    robot.chassis.move(y=10)


def deliver_sample(robot: robot.Robot):
    sample_color_low = (0, 0, 0)
    sample_color_high = (360, 100, 100)
    # 识别样本的颜色
    color_result = robot.skill.detect_color_blob(
        YELLOW_LOW, YELLOW_HIGH)
    print(color_result)
    if color_result[0]:
        sample_color_low = YELLOW_LOW
        sample_color_high = YELLOW_HIGH
    else:
        sample_color_low = PURPLE_LOW
        sample_color_high = PURPLE_HIGH
    # 抓取样本
    move_to_position(robot, sign=SAMPLE)
    grab(robot)
    robot.chassis.move(y=-14)
    robot.chassis.move(x=38)
    # 前往消毒室
    robot.chassis.move(a=180)
    drive_line(robot)
    color_result = robot.skill.detect_color_blob(
        sample_color_low, sample_color_high, timeout=10)
    if color_result[0]:
        if color_result[1][2] < 700:
            time.sleep(0.1)
            color_result = robot.skill.detect_color_blob(
                sample_color_low, sample_color_high)
    # 放到消毒转盘上的对应区域
    robot.arm.move_to(y=13, z=10)
    robot.chassis.move(y=2)
    robot.gripper.open()
    robot.chassis.move(y=-2)
    robot.servo.reset()
    robot.chassis.move(y=-15)
    # 离开消毒室，前往药房
    robot.chassis.move(a=90)
    robot.chassis.move(x=5)
    drive_line(robot)
    robot.chassis.move(a=90)


def get_medicine(robot: robot.Robot):
    move_to_position(robot, sign=MEDICINE)
    robot.arm.move_to(y=14, z=8)
    robot.chassis.move(y=2)
    robot.gripper.close()
    robot.arm.move_to(y=14, z=10)
    robot.chassis.move(y=-5)
    robot.servo.reset()


def move_to_ward(robot: robot.Robot):
    robot.chassis.move(a=90)
    drive_line(robot)
    robot.chassis.move(a=90)
    drive_line(robot)
    robot.chassis.move(a=90)


def deliver_medicine(robot: robot.Robot):
    get_medicine(robot)
    robot.chassis.move(y=-10)
    move_to_ward(robot)
    move_to_position(robot, sign=MEDICINE_PLACE)
    put_down(robot)


def knock_on(robot: robot.Robot):
    robot.arm.move_to(y=12, z=10)
    time.sleep(0.1)
    robot.servo.reset()


def assist_patient(robot: robot.Robot):
    robot.chassis.move(a=180)
    time.sleep(1)
    robot.chassis.move(x=-20)
    move_to_position(robot, sign=BUTTON, distance=14)
    robot.chassis.move(y=5)
    robot.gripper.close()
    # TODO:机器学习
    gesture_id = PALM
    if gesture_id == PALM:
        knock_on()
    else:
        knock_number = 0
        while knock_number < 2:
            knock_on(robot)
            knock_number = knock_number+1


def return_terminus(robot: robot.Robot):
    robot.chassis.move(y=-10)
    robot.chassis.move(a=-90)
    drive_line(robot, line_stop=LINE_CROSS)
    robot.chassis.move(y=20)
    robot.chassis.move(x=5)
    robot.chassis.move(a=-90)
    robot.chassis.move(y=-20)


if __name__ == '__main__':
    name = 'GomerX_kbnAcF'
    gomerx = robot.Robot(name)
    clean_garbage(gomerx)
    guide_patient(gomerx)
    deliver_sample(gomerx)
    deliver_medicine(gomerx)
    assist_patient(gomerx)
    return_terminus(gomerx)

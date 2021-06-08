from gomerx import robot
import time

if __name__ == '__main__':
    # robot_name = input('Please input robot name: ')
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)

    chassis = my_robot.chassis

    ''' 走一个正方形'''
    # 前进80cm
    chassis.move(x=0, y=80, a=0, wait_for_complete=True)
    # 右移80cm
    chassis.move(x=80, y=0, a=0, wait_for_complete=True)
    # 后退80cm
    chassis.move(x=0, y=-80, a=0, wait_for_complete=True)
    # 左移80cm
    chassis.move(x=-80, y=0, a=0, wait_for_complete=True)

    ''' 再走一个正方形'''
    for i in range(4):
        # 前进80cm
        chassis.move(x=0, y=80, a=0, wait_for_complete=True)
        # 右转90°
        chassis.move(x=0, y=0, a=90, wait_for_complete=True)

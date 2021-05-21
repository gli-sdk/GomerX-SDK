import time
from gomerx import robot

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_arm = my_robot.arm
    my_arm.move_to(12, 10)
    my_arm.move_to(12, 15)

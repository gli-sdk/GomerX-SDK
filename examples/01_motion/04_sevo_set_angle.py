import time
from gomerx import robot

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_servo = my_robot.servo
    my_servo.move_to(0, 180)
    my_servo.move_to(1, 70)

import time
from gomerx import robot
from gomerx import led

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_led = my_robot.led

    color = (255, 255, 255)  # r, g, b
    my_led.set_led(color, led.EFFECT_ON)
    time.sleep(3)
    color = (0, 0, 0)
    my_led.set_led(color, led.EFFECT_OFF)

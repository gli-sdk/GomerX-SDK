import time
from gomerx import robot
from gomerx import led

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_led = my_robot.led

    color = (128, 0, 50)  # r, g, b
    my_led.set_led(color=color, effect=led.EFFECT_FLASH, T=500)
    time.sleep(5)
    my_led.set_led(color=(0, 0, 0), effect=led.EFFECT_OFF)
    my_robot.close()
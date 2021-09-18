from gomerx import robot
from configparser import ConfigParser
import os

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    cwd = os.getcwd()
    print(cwd)
    config = ConfigParser()
    config.read(cwd+'\\firmware\\update.ini')
    update_file = cwd+'\\firmware\\update.tgz'
    ver = config.get('info', 'ver')
    info = 'ver:' + ver
    my_robot._conn.send_file(2, update_file, info)
    print('updating, please wait GomerX reboot!')
    my_robot.close()
from gomerx import robot

if __name__ == '__main__':
    # robot_name = input('Please input robot name: ')
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    version = my_robot.get_version()
    print("Robot Version: ", version)
    sn = my_robot.get_sn()
    print("Robot SN: ", sn)
    battery = my_robot.get_battery()
    print("Robot Battery: ", battery)

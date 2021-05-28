from gomerx import robot

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_gripper = my_robot.gripper
    my_gripper.close()
    my_gripper.open()
    my_robot.close()

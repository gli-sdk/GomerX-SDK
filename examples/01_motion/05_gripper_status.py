from gomerx import robot

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_gripper = my_robot.gripper
    gripper_status = my_gripper.get_status()
    print("gripper status: ", gripper_status)
    
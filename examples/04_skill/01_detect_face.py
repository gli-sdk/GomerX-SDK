from gomerx import robot

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_skill = my_robot.skill

    result = my_skill.detect_face()
    if result:
        print("Found face")
    else:
        print("Not Found face")
    my_robot.close()

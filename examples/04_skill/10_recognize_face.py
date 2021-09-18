from gomerx import robot
if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    if my_robot.skill.detect_face():
        result, name = my_robot.skill.recognize_face()
        if result:
            print("recognize face as ", name)
        else:
            print("unknown face")
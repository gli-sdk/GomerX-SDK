from gomerx import robot
if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    if my_robot.skill.detect_face(timeout=0):
        name = "001_Tom"
        if my_robot.skill.save_face(name):
            print("Save face OK! ")
        else:
            print("Save face failed! ")
    else:
        print("No face detected!")
    result, face_list = my_robot.skill.get_face_list()
    print("face list: ", face_list)
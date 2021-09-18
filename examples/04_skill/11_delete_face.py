from gomerx import robot
if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    result, face_list = my_robot.skill.get_face_list()
    print("face list: ", face_list)
    if len(face_list) > 0:
        name = face_list[0]
        if my_robot.skill.delete_face(name):
            print('delete ', name, ' ok!')
        else:
            print('delete ', name, ' failed!')
    
    result, face_list = my_robot.skill.get_face_list()
    print("new face list: ", face_list)

        
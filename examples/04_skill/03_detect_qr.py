from gomerx import robot

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_skill = my_robot.skill
    my_camera = my_robot.camera

    result, data = my_skill.detect_qrcode()
    if result:
        print("Found qrcode: ", data)
    else:
        print("Not Found qrcode")

    my_robot.close()

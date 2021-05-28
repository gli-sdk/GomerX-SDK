from gomerx import robot

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_skill = my_robot.skill

    # 设置蓝色的HSV值上下限
    hsv_low = (220, 20, 20)
    hsv_high = (260, 100, 100)

    result, line = my_skill.detect_line(hsv_low, hsv_high)

    if result:
        print("Found blue line!")
        my_skill.move_along_line()
    else:
        print("Not found blue line.")
    my_robot.close()

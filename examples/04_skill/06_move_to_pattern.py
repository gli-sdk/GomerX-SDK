from gomerx import robot

if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_skill = my_robot.skill

    pattern_id = 'B'
    result = my_skill.detect_pattern(id=pattern_id)
    if result:
        print("Found pattern {}".format(pattern_id))
        my_skill.move_to_pattern(pattern_id, x=0, y=13)
    else:
        print("Not Found pattern {}".format(pattern_id))
    my_robot.close()

import time
from gomerx import robot

if __name__ == '__main__':
    # robot_name = input('Please input robot name: ')
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_camera = my_robot.camera
    my_camera.start_video_stream(display=True)
    time.sleep(5)
    my_camera.stop_video_stream()
    my_robot.close()

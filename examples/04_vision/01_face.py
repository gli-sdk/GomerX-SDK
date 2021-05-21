import time
from gomerx import robot


class FaceInfo(object):
    def __init__(self, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h


faces = []


def on_detect_face(face_info: FaceInfo):
    num = len(face_info)
    faces.clear()
    for i in range(0, num):
        x, y, w, h = face_info[i]
        faces.append(FaceInfo(x, y, w, h))
        print("face: x:{}, y:{}, w:{}, h:{}".format(x, y, w, h))


if __name__ == '__main__':
    robot_name = 'GomerX_6e09ba'
    my_robot = robot.Robot(robot_name)
    my_camera = my_robot.camera
    my_vision = my_robot.vision

    result = my_vision.sub_detect_info(name='face', callback=on_detect_face)
    time.sleep(3)
    result = my_vision.unsub_detect_info(name='face')

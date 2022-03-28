

from enum import IntEnum, unique
import json
from . import counter


Heartbeat = 1001
SearchDevice = 1002
SendFileReq = 2001
SendFileRsp = 2002
Video = 2003
Update = 2004
MotorCtrl = 2005
ChassisXYA = 2006
ChassisWheel = 2007
ArmEndPos = 2008
ArmServoAngle = 2009
ArmCalib = 2010
Gripper = 2011
DetFace = 2012
CapImg4Face = 2013
DetPattern = 2014
DetQrCode = 2015
CapImg4ML = 2016
Move2Pattern = 2017
DetColor = 2018
DetLine = 2019
FollowLine = 2020
FollowLinePID = 2021
StopMotion = 2022
SetLed = 2023
Recover = 2024
Connect = 9998
Disconnect = 9999


class DeviceContent:
    def __init__(self, version='', name='', battery=0, info: dict = None):
        if info is not None:
            self.fromDict(info)
        else:
            self.version = version
            self.name = name
            self.battery = battery

    def toDict(self):
        return self.__dict__

    def fromDict(self, d: dict):
        for k, v in d.items():
            self.__setattr__(k, v)


class Message(object):

    _counter = counter.Counter()

    def __init__(self, type: int = 0, dataint: list = [], datastr: str = '', result: int = 100, device: DeviceContent = None, message: str = ''):
        if message != '':
            self.fromString(message)
        else:
            self.type = type
            self.seq = Message._counter.next()
            self.dataint = dataint
            self.datastr = datastr
            self.device = device
            self.result = result

    def toString(self) -> str:
        data = {}
        if self.seq >= 0:
            data['seq'] = self.seq
        if self.type != 0:
            data['type'] = self.type
        if self.dataint != []:
            data['dataint'] = self.dataint
        if self.datastr != '':
            data['datastr'] = self.datastr
        if self.result != 0:
            data['result'] = self.result
        if self.device != None:
            data['device'] = self.device
        return json.dumps(data)

    def fromString(self, str: str):
        j = json.loads(str)
        self.type = j.get('type', 0)
        self.seq = j.get('seq', 0)
        self.dataint = j.get('dataint', [])
        self.datastr = j.get('datastr', '')
        self.result = j.get('result', 100)
        self.device = j.get('device')
        if self.device is not None:
            self.device = DeviceContent(info=self.device)

    def isTypeOf(self, type: int) -> bool:
        return self.type == type


from ctypes import *
from queue import Empty, Full, Queue
import socket
import threading
import time
from . import event
from . import message
from . import netutil

import cv2
from .exceptions import RobotConnectFailed, RobotNotSearched


class Client(object):
    # 唯一客户端

    AP = 'ap'
    Router = 'router'
    SearchPort = 20000
    TCPPort = 9009
    FilePort = 17000
    VideoPort = 16016

    BufSize = 1400

    isConnected = False
    isHealthy = False
    # 客户端状态

    tcpSendQueue = Queue()
    tcpRecvQueue = Queue()
    _instance_lock = threading.Lock()

    def __init__(self, robot: str, mode=AP) -> None:
        self.searchSocket = None
        self.mode = mode
        self.robot = robot
        self.battery = 0
        self.version = '0.0.0'

        self.halfMessage = ''

        self.currentHeartbeat = 0
        self.lastHeartbeatResponseTime = 0

        self.tcpSocket = None
        self.fileSocket = None

        self.ip = netutil.getIP(self.mode)
        self.broadcastIP = netutil.getBroadcastIP(self.ip)

        self.search()
        self.connect()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Client, "_instance"):
            with Client._instance_lock:
                if not hasattr(Client, "_instance"):
                    Client._instance = object.__new__(cls)
        return Client._instance

    @staticmethod
    def send(m: message.Message) -> bool:
        if not Client.isConnected:
            return False
        try:
            Client.tcpSendQueue.put_nowait(m)
        except Full:
            return False
        return True

    def searchSend(self):
        # 每0.2s 发送一次消息，共发送3次
        for i in range(3):
            mess = message.Message(message.SearchDevice)
            self.searchSocket.sendto(
                mess.toString().encode(), (self.broadcastIP, Client.SearchPort))
            time.sleep(0.2)

    def search(self):
        # 搜索机器人
        self.searchSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.searchSocket.settimeout(2)
        searchSendThread = threading.Thread(
            target=self.searchSend, name='searchSendThread')
        searchSendThread.start()

        start = time.time()
        searched = False
        while (not searched) and (time.time() - start < 2):
            time.sleep(0.1)
            data, addr = self.searchSocket.recvfrom(Client.BufSize)
            msg = message.Message(message=data.decode())
            if (msg.device.name == self.robot):
                searched = True
                self.serverIP = addr[0]
        print('search done ', self.serverIP)

        if not searched:
            raise RobotNotSearched()

    def connect(self):
        # 连接
        mess = message.Message(message.Connect)
        self.searchSocket.sendto(
            mess.toString().encode(), (self.serverIP, Client.SearchPort))

        connected = False
        start = time.time()

        while(time.time() - start < 1.5) and (not connected):
            data, addr = self.searchSocket.recvfrom(Client.BufSize)
            r = message.Message(message=data.decode())
            if r.isTypeOf(message.Connect):
                connected = True
                self.battery = r.device.battery
                self.version = r.device.version
            time.sleep(0.05)
        if not connected:
            raise RobotConnectFailed

        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.tcpSocket.connect((self.serverIP, Client.TCPPort))

        Client.isConnected = True
        Client.isHealthy = True

        # 启动收发线程
        self.lastMsgTime = time.time()
        self.lastHeartbeatTime = time.time()

        tcpRecvThread = threading.Thread(
            target=self.tcpRecv, name='tcpRecvThread')
        tcpRecvThread.setDaemon(True)
        tcpRecvThread.start()
        tcpSendThread = threading.Thread(
            target=self.tcpSend, name='tcpSendThread')
        tcpSendThread.setDaemon(True)
        tcpSendThread.start()

        heartbeatThread = threading.Thread(
            target=self.heartbeat, name='heartbeatThread')
        heartbeatThread.setDaemon(True)
        heartbeatThread.start()

    def tcpSend(self):
        # tcp 发送线程
        while not netutil.isClosed(self.tcpSocket):
            try:
                m = self.tcpSendQueue.get_nowait()
                data = m.toString() + '\n'
                self.tcpSocket.send(data.encode())
            except Empty:
                continue
            time.sleep(0.05)
        self.tcpSocket.close()

    def tcpRecv(self):
        # tcp 接收线程
        while not netutil.isClosed(self.tcpSocket):
            data = self.tcpSocket.recv(Client.BufSize)
            self.unPack(data.decode())
        self.tcpSocket.close()

    def unPack(self, data):
        # 解包TCP消息
        end = False
        while not end:
            position = data.find('\n')
            if (position == -1):
                self.halfMessage += data
                end = True
            elif position == len(data) - 1:
                m = self.halfMessage + data[:-1]
                self.handleMessage(m)
                self.halfMessage = ''
                end = True
            else:
                m = self.halfMessage + data[:position]
                self.handleMessage(m)
                self.halfMessage = ''
                data = data[position+1:]

    def handleMessage(self, m):
        # 处理消息
        msg = message.Message(message=m)
        if msg.isTypeOf(message.Heartbeat):
            self.checkHeartbeatResponse()
        else:
            self.lastMsgTime = time.time()
            if msg.result != 100:
                event.Dispatcher().recv(msg)

    def checkHeartbeatResponse(self):
        self.lastHeartbeatTime = time.time()
        self.currentHeartbeat = 0
        gap = self.lastHeartbeatTime - self.heartbeatStart

        if Client.isConnected and (not Client.isHealthy) and gap < 1 and self.lastHeartbeatResponseTime < 1:
            Client.isHealthy = True
        self.lastHeartbeatResponseTime = gap

    def heartbeat(self):
        # 心跳
        self.sendHeartbeat()
        while not netutil.isClosed(self.tcpSocket):
            now = time.time()
            msgGap = now - self.lastMsgTime
            beatGap = now - self.lastHeartbeatTime

            if beatGap > 115:
                self.disconnect()
            elif beatGap > 6:
                Client.isHealthy = False
            elif beatGap > 4:
                self.sendHeartbeat()
            elif beatGap > 3 and msgGap > 2:
                self.sendHeartbeat()
            time.sleep(0.05)

    def sendHeartbeat(self):
        # 发送心跳
        if (self.currentHeartbeat != 0):
            return
        m = message.Message(type=message.Heartbeat)
        Client.send(m)

        self.currentHeartbeat = m.seq
        self.heartbeatStart = time.time()

    def disconnect(self):
        # 断开连接并清空状态
        print('disconnect')

        if Client.isConnected:
            Client.send(message.Message(type=message.Disconnect))
            time.sleep(0.5)
            Client.isConnected = False
            Client.isHealthy = False

        if self.tcpSocket is not None:
            self.tcpSocket.close()
        if self.fileSocket is not None:
            self.fileSocket.close()

        time.sleep(0.5)

        Client.tcpSendQueue.queue.clear()
        Client.tcpRecvQueue.queue.clear()

    def connectFile(self):
        # 连接文件socket
        if self.fileSocket is None:
            self.fileSocket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM, 0)
            self.fileSocket.settimeout(2)
            self.fileSocket.connect((self.serverIP, Client.FilePort))

    def receiveFile(self, path, size):
        # 接收文件
        self.connectFile()
        with open(path, 'wb') as f:
            while((size > 0)):
                data, addr = self.fileSocket.recv(Client.BufSize)
                size -= len(data)
                f.write(data)

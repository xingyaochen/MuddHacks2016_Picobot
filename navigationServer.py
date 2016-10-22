import socket
from threading import Thread
import time
import RobotSteer
import RPi.GPIO as io
import time
from navigationServer import *
io.setmode(io.BOARD)
io.setup(18, io.OUT)  #left forward
io.setup(22, io.OUT)    #left reverse
io.setup(15, io.OUT)    #right forward
io.setup(16, io.OUT)    #right reverse"""

HOST = '0.0.0.0'
PORT = 8800
class NavigationPoller(object):
    HOST = '0.0.0.0'
    PORT = 8800
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((HOST, PORT))
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()
	self.fnum = -1
        self.x = -1
        self.y = -1
        self.theta = -1
        self.error = ""

    # create thread for capturing images
    def start(self):
        Thread(target=self._update_frame, args=()).start()

    def _update_frame(self):
	try:
            while True:
                data = self.conn.recv(1024)
                if not data: break
                if "#" in data: data = data[:data.index("#")]
                data = data.decode("UTF-8")
                try:
                    self.fnum, self.x, self.y, self.theta = tuple(map(float, data.split(":")[:3]))
                except: break
        except Exception as e: self.error = str(e)
	finally: self.conn.close()

    # get the current frame
    def get_current_info(self):
        return (self.fnum, self.x, self.y, self.theta, self.error)

if __name__ == "__main__":
    # test = NavigationPoller()
    # test.start()
    RobotSteer.stop()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    while True:
        data = conn.recv(1024)
        #if len(data) > 51: data = data[:51]
        if "#" in data: data = data[:data.index("#")]
        if not data: break
        data = data.decode("UTF-8")
        print(data)
        #try:
        try:
            fnum, x, y, theta = tuple(map(float, data.split(":")))
        except: continue
        print(theta)
        # RobotSteer.right(0.001)
        if theta > 180:
            RobotSteer.right(0.001)
        else:
            RobotSteer.left(0.001)
        time.sleep(0.01)
        RobotSteer.stop()
        if abs(180 - theta) < 30:
            time.sleep(0.02)
        else:
            time.sleep(0.01)

        #except: break

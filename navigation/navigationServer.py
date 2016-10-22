import socket
from threading import Thread
import time

class NavigationPoller(object):
    HOST = '0.0.0.0'
    PORT = 8800
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()
        self.x = -1
        self.y = -1
        self.theta = -1

    # create thread for capturing images
    def start(self):
        Thread(target=self._update_frame, args=()).start()

    def _update_frame(self):
        while True:
            data = self.conn.recv(1024)
            if not data: break
            data = data.decode("UTF-8")
            self.x, self.y, self.theta = tuple(map(float, data.split(" ")))

    # get the current frame
    def get_current_info(self):
        return (self.x, self.y, self.theta)

if __name__ == "__main__":
    test = NavigationPoller()
    test.start()

    while True:
        print(test.get_current_info());

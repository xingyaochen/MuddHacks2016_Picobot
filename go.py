import RobotSteer
import RPi.GPIO as io
import time
from navigationServer import *
io.setmode(io.BOARD)
io.setup(18, io.OUT)  #left forward
io.setup(22, io.OUT)    #left reverse
io.setup(15, io.OUT)    #right forward
io.setup(16, io.OUT)    #right reverse"""

print("hi!")
test = NavigationPoller()
test.start()
while True:
    _, _, theta, _, _ = test.get_current_info()
    print(theta)
    if theta > 0:
	RobotSteer.right(0.001)
    else:
	RobotSteer.left(0.001)
    time.sleep(0.001)

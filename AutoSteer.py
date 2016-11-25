import RobotSteer
import RPi.GPIO as io
import time
import sys, tty, termios

io.setmode(io.BOARD)
io.setwarnings(False)

io.setup(18, io.OUT)
io.setup(22, io.OUT)
io.setup(15, io.OUT)
io.setup(16, io.OUT)

io.setup(7, io.IN, pull_up_down=io.PUD_UP)
io.setup(11, io.IN, pull_up_down=io.PUD_UP)
io.setup(12, io.IN, pull_up_down=io.PUD_UP)
io.setup(13, io.IN, pull_up_down=io.PUD_UP)

while True:
    if RobotSteer.IRDetect()[0] == 0 or RobotSteer.IRDetect()[2] == 0:
	RobotSteer.left(0.010)
	time.sleep(0.001)
	RobotSteer.stop()
	time.sleep(0.003)
    else:
	RobotSteer.forward(0.005)
	time.sleep(0.001)
	RobotSteer.stop()
	time.sleep(0.010)

io.cleanup()
 

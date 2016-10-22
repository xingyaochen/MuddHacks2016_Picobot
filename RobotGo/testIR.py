import RPi.GPIO as io
import time
import sys, tty, termios

io.setmode(io.BOARD)
io.setwarnings(False)

def IRDetect():
    """returns booleans of obstacles in front, back, left, right"""
    io.setup(7, io.IN, pull_up_down=io.PUD_UP) #IR  
    io.setup(11, io.IN, pull_up_down=io.PUD_UP) #IR back
    io.setup(12, io.IN, pull_up_down=io.PUD_UP) #IR left
    io.setup(13, io.IN, pull_up_down=io.PUD_UP) #IR right
    front=io.input(7)
    back=io.input(11)
    right=io.input(12)
    left=io.input(13)
    return tuple([front, back, left, right])


io.setup(7, io.IN, pull_up_down=io.PUD_UP) #IR  
io.setup(11, io.IN, pull_up_down=io.PUD_UP) #IR back
io.setup(12, io.IN, pull_up_down=io.PUD_UP) #IR left
io.setup(13, io.IN, pull_up_down=io.PUD_UP) #IR right
front=io.input(7)
back=io.input(11)
right=io.input(12)
left=io.input(13)
if left==0:
    print("left")
if right==0:
    print("left")
if front==0:
    print("left")
if back==0:
    print("left")

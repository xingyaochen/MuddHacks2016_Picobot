#import RPi.GPOI as io
import sys, tty, termios
import time
import atexit
#import Robot
#from Adafruit_MotorHAT import Adafruit_MotorHAT


#io.setmode(io.BOARD)
#io.setwarnings(False)


def IRDetect():
    """returns booleans of obstacles in front, back, left, right"""
    io.setup(7, io.IN, pull_up_down=io.PUD_UP) #IR front
    io.setup(11, io.IN, pull_up_down=io.PUD_UP) #IR back
    io.setup(12, io.IN, pull_up_down=io.PUD_UP) #IR left
    io.setup(13, io.IN, pull_up_down=io.PUD_UP) #IR right
    front=io.input(7)
    back=io.input(11)
    right=io.input(12)
    left=io.input(13)
    return tuple([front, back, left, right])


def getch():
    fd=sys.stdin.fileno()
    old_settings=termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch=sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def manualSteer(debug=True):
    """run this to steer PicoBot using keyboard, press 'w', 'a', 's', 'z'. """
    LEFT_TRIM   = 0
    RIGHT_TRIM  = 0
    robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)
    while True:
        char=getch()
        if debug:
            print(char)
        if(char=="w"):
            robot.forward(150, 0.05)
        if(char=="a"):
            robot.left(150, 0.05)
        if(char=="s"):
            robot.right(150, 0.05)
        if(char=="z"):
            robot.forward(150, 0.05)
        if(char==" "):
            robot.stop()
            if debug:
                print("TERMINATE")
            break

def autoSteer(IRSensors):
    """takes a list of length 4 of IR sensor pins"""
    return
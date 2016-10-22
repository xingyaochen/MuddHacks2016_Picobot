import RPi.GPIO as io
import time
import sys, tty, termios

io.setmode(io.BOARD)
io.setwarnings(False)


io.setup(18, io.OUT)  #left forward
io.setup(22, io.OUT)    #left reverse
io.setup(15, io.OUT)    #right forward
io.setup(16, io.OUT)    #right reverse"""
"""io.setup(15, io.IN, pull_up_down=io.PUD_UP) #IR front
io.setup(7, io.IN, pull_up_down=io.PUD_UP) #IR back
io.setup(18, io.IN, pull_up_down=io.PUD_UP) #IR right
io.setup(5, io.IN, pull_up_down=io.PUD_UP) #IR left
"""


def setMotors(left1, left2, right1, right2, debug=True):
    """define GPIO pins that correspont to the motor controls, takes ints"""
    io.setup(left1, io.OUT)  #left forward
    io.setup(left2, io.OUT)    #left reverse
    io.setup(right1, io.OUT)    #right forward
    io.setup(right2, io.OUT)    #right reverse
    if debug:
        print("lefts:" [left1, left2])
        print("rights:" [right1, right2])
    return [left1, left2, right1, right2]

motors=[18, 22, 16, 15]

def forward(num, debug=True):
    """takes in an int for time, and a list of len 4 for motors"""
    if debug:
        print("forward")
    io.output(motors[0], 1) #move left1 motor
    io.output(motors[1],0) #don't move left2 motor
    io.output(motors[2],1) #move right1 motor
    io.output(motors[3],0) #dont move right2 motor
    time.sleep(num)

def back(num, debug=True):
    """takes in an int for time, and a list of len 4 for motors"""
    if debug:
        print("backward")
    io.output(motors[0], 0) #stop left1 motor
    io.output(motors[1],1) #move left2 motor
    io.output(motors[2],0) #stop right1 motor
    io.output(motors[3],1) #move right2 motor
    time.sleep(num)

def right(num,debug=True):
    """takes in an int for time, and a list of len 4 for motors"""
    if debug:
        print("turn right")
    io.output(motors[0], 1) #move left1 motor
    io.output(motors[1],0) #stop left2 motor
    io.output(motors[2],0) #stop right1 motor
    io.output(motors[3],1) #move right2 motor
    time.sleep(num)

def left(num, debug=True):
    """takes in an int for time, and a list of len 4 for motors"""
    if debug:
        print("turn left")
    io.output(motors[0], 0) #stop left1 motor
    io.output(motors[1],1) #move left2 motor
    io.output(motors[2],1)# move right1 motor
    io.output(motors[3] ,0) #stop right2 motor
    time.sleep(num)

def stop(debug=True):
    """takes in an int for time, and a list of len 4 for motors"""
    if debug:
        print("stop")
    io.output(motors[0], 0) #stop all motors
    io.output(motors[1],0)
    io.output(motors[2],0)
    io.output(motors[3],0)


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
    while True:
        char=getch()
        if debug:
            print(char)
        if(char=="w"):
            forward(0.05)
        if(char=="s"):
            right(0.05)
        if(char=="a"):
            left(0.05)
        if(char=="z"):
            back(0.05)
        if(char==" "):
            if debug:
                print("TERMINATE")
            stop()
            break

def autoSteer(IRSensors):
    """takes a list of length 4 of IR sensor pins"""
    return



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


def getch():
    fd=sys.stdin.fileno()
    old_settings=termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch=sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

"""
def manualSteer(debug=True):
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
"""
io.cleanup()

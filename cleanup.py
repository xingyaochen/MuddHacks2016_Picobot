import RPi.GPIO as io
io.setmode(io.BOARD)
motors=[18, 22, 16, 15]
left1=15
left2=16
right1=18
right2=22
io.setup(left1, io.OUT)  #left forward
io.setup(left2, io.OUT)    #left reverse
io.setup(right1, io.OUT)    #right forward
io.setup(right2, io.OUT)
io.cleanup()  


import RobotSteer

while True:
    if IRDetect()[0] == 0:
	left(0.005)
    else:
	forward(0.005)

io.cleanup()
 

"""

Programa principal
"""
import numpy as np
import time
import math as m
import sys
import sim as vrep # access all the VREP elements
import pathcontrol as pc
import sfla

#<---------------------------------Initialization--------------------------------------->
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',-1,True,True,5000,5) # start a connection
if clientID!=-1:
	print ('Connected to remote API server')
else:
	print('Not connected to remote API server')
	sys.exit("No connection")

# Getting handles for the motors and robot
err, motorL = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_blocking)
err, motorR = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_blocking)
err, robot = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx', vrep.simx_opmode_blocking)

# Assigning handles to the ultrasonic sensors
usensor = []
for i in range(1,17):
    err, s = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_ultrasonicSensor'+str(i), vrep.simx_opmode_blocking)
    usensor.append(s)

# Sensor initialization
for i in range(16):
    err, state, point, detectedObj, detectedSurfNormVec = vrep.simxReadProximitySensor(
        clientID, usensor[i], vrep.simx_opmode_streaming)


#<-----------------------------------Control----------------------------------------->

# Create an instance of the solver
path_solver = sfla.sflaSolver(30, 5, 7, 12, 0.5)
target = np.array([3,-3.85])
ret, cur_pos = vrep.simxGetObjectPosition(clientID, robot, -1, vrep.simx_opmode_oneshot)
path = np.empty((0,2))
cur_pos = np.array(cur_pos[:2])
while np.linalg.norm(target - cur_pos) > 0.4:
    obstacles = pc.sense_obstacles(clientID, usensor)
    cur_pos, frogs, memeplexes = path_solver.sfla(cur_pos, target, obstacles)
    print(cur_pos)
    while True:
        errp, ulc, urc, pos, rot = pc.continuosControl(clientID, robot, cur_pos)
    #path = np.vstack((path, pos))
        errf = vrep.simxSetJointTargetVelocity(clientID, motorL, ulc, vrep.simx_opmode_streaming)
        errf = vrep.simxSetJointTargetVelocity(clientID, motorR, urc, vrep.simx_opmode_streaming)
        if ulc == 0 and urc == 0:
            break


# The End
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)

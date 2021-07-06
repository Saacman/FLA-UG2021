import b0RemoteApi as b0
import time

with b0.RemoteApiClient('b0RemoteApi-python', 'b0RemoteApi')as client:
    client.simxAddStatusbarMessage('Hello',client.simxDefaultPublisher())
    client.simxStartSimulation(client.simxDefaultPublisher())
    t = time.time()
    i = 0
    while time.time()-t< 30:
        #client.simxAddStatusbarMessage('Hello {i}',client.simxDefaultPublisher())
        i = i +1


    client.simxStopSimulation(client.simxDefaultPublisher())
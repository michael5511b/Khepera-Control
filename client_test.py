import socket
import sys
import time
import math
import numpy as  np
import matplotlib.pyplot as plt 

clientsocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host1 = socket.gethostbyname('192.168.1.150')
clientsocket1.connect((host1, 3000))


bx = 1.799556
by = -0.103884
bz = -0.893244

start = time.time()
Time = '0.0'

#t = 0
Time_val = []
t_old = 0.0
t_old_khepera = 0.0
F1 = []
F2 = []
i = 0
while (t_old <= 10):
	end = time.time()
	#t = end - start
	t_new = end - start
	#print 1/(t_new - t_old)
	if i > 1:
		F1.append(1/(t_new - t_old))
	t_old = t_new


	W = '0'
	#V = str(200 - float(Time) * 30)
	#V = str(500 * math.sin(2 * 3.14159 * float(Time)))
	#V = '200'	
	V = '0'
	clientsocket1.send(W + 'x' + V)

	data = clientsocket1.recv(4096)
	#time.sleep(0.105)
	
	Time = data.split('T')[1]

	t_new_khepera = float(Time)
	#print 1/(t_new_khepera - t_old_khepera)
	if i > 1:
		F2.append(1/(t_new_khepera - t_old_khepera))
		Time_val.append(t_new)
	t_old_khepera = t_new_khepera
	i = i+1

	
"""
	AX = data.split('AX')[1]
	AY = data.split('AY')[1]
	AZ = data.split('AZ')[1]

	GX = data.split('GX')[1]
	GY = data.split('GY')[1]
	GZ = data.split('GZ')[1]

	
	UA = data.split('UA')[1]
	UB = data.split('UB')[1]
	UC = data.split('UC')[1]
	UD = data.split('UD')[1]
	UE = data.split('UE')[1]

	IA = data.split('IA')[1]
	IB = data.split('IB')[1]
	IC = data.split('IC')[1]
	ID = data.split('ID')[1]
	IE = data.split('IE')[1]
	IF = data.split('IF')[1]
	IG = data.split('IG')[1]
	IH = data.split('IH')[1]
	II = data.split('II')[1]
	IJ = data.split('IJ')[1]
	IK = data.split('IK')[1]
	IL = data.split('IL')[1]
	
	
	PL = data.split('PL')[1]
	PR = data.split('PR')[1]

	SL = data.split('SL')[1]
	SR = data.split('SR')[1]

	# Gyro after calibration
	GX = str(float(GX) - bx)
	GY = str(float(GY) - by)
	GZ = str(float(GZ) - bz)

	# Encoder/motor speed in mm/sec
	sL = str(float(SL) * 0.678181)
	sR = str(float(SR) * 0.678181)

	# Khepera speed
	vel = str((float(sL)+float(sR))/2)
 """
	#print "Time: " + str(t) + "sec\n" + "ec1: " + str(ec1) + "\n" + "ec2: " + str(ec2) + "\n" + "em1: " + str(em1) + "\n" + "em2: " + str(em2) + "\n" 

	#print "================================================="

	#print "Time: " + Time + "\n" 
	#print "\nAccerleration on X: " + AX + "\nAccerleration on Y: " + AY + "\nAccerleration on Z: " + AZ + "\n"  
	#print "\nAngular rate (Gyroscope) on X: " + GX + "\nAngular rate (Gyroscope) on Y: " + GY + "\nAngular rate (Gyroscope) on Z: " + GZ + "\n" 
	#print "\nEncoder position left: " + PL + "\nEncoder position right: " + PR + "\n"
	#print "\nEncoder speed left: " + SL + "\nEncoder pspeed right: " + SR + "\n" 
	#print "\nEncoder speed left (in mm/sec): " + sL + "\nEncoder pspeed right (in mm/sec): " + sR + "\n"
	#print "\nKhepera robot velocity: " + vel + "\n"
	#print "\nUltrasconic sensor 1: " + UA + "\nUltrasconic sensor 2: " + UB + "\nUltrasconic sensor 3: " + UC + "\nUltrasconic sensor 4: " + UD + "\nUltrasconic sensor 5: " + UE + "\n"
	#print "\nInfrared sensor 1: " + IA + "\nInfrared sensor 2: " + IB + "\nInfrared sensor 3: " + IC + "\nInfrared sensor 4: " + ID + "\nInfrared sensor 5: " + IE + "\nInfrared sensor 6: " + IF + "\nInfrared sensor 7: " + IG + "\nInfrared sensor 8: " + IH + "\nInfrared sensor 9: " + II + "\nInfrared sensor 10: " + IJ + "\nInfrared sensor 11: " + IK + "\nInfrared sensor 12: " + IL + "\n"

	#print "================================================="

plt.plot(Time_val, F1,'-b') 
plt.plot(Time_val, F2,'-r') 

plt.xlabel('Time') 
plt.show()

while True:
	W = '0'
	V = '0'
	clientsocket1.send(W + 'x' + V)




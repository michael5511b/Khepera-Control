import socket
import sys
import time
import math
import numpy as  np
import matplotlib.pyplot as plt 

clientsocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#clientsocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host1 = socket.gethostbyname('192.168.1.154')
#host2 = socket.gethostbyname('192.168.1.154')
clientsocket1.connect((host1, 3000))
#clientsocket2.connect((host1, 3001))
#clientsocket2.connect((host2, 3000))

# clientsocket.send('hello')
""" 
#Daily Calibration
count = 0
bx = 0
by = 0 
bz = 0
M  = 50

print "Gyroscope calibration in progress...."

while count<M:

	count = count+1
	data = clientsocket1.recv(2048)
	
	v1 = data.split('T')
	Time = v1[0]
	v2 = v1[1].split('AX')
	AX = v2[0]
	v3 = v2[1].split('AY')
	AY = v3[0]
	v4 = v3[1].split('AZ')
	AZ = v4[0]
	v5 = v4[1].split('GX')
	 
	bx = bx + float(v5[0])

	v6 = v5[1].split('GY')

	by = by + float(v6[0])

	v7 = v6[1].split('GZ')

	bz = bz + float(v7[0])
        #print Time



bx = bx/M
by = by/M
bz = bz/M


 
print bx
print by
print bz

"""

bx = 1.799556
by = -0.103884
bz = -0.893244

start = time.time()
Time = '0.0'

E1c = []
Time_val = []
t = 0
while (t<12):
	end = time.time()
	t = end - start
	W = '0'
	V = str(200 - float(Time) * 30)
	#V = str(500 * math.sin(2 * 3.14159 * float(Time)))
	#V = '200'	

	#clientsocket1.send(W)
	#time.sleep(0.105)
	clientsocket1.send(W + 'x' + V)
	#print t
	data = clientsocket1.recv(4096)
	time.sleep(0.105)
	
	v1 = data.split('T')
	Time = v1[0]

	v2 = v1[1].split('AX')
	AX = v2[0]
	v3 = v2[1].split('AY')
	AY = v3[0]
	v4 = v3[1].split('AZ')
	AZ = v4[0]

	v5 = v4[1].split('GX')
	GX = v5[0] 
	v6 = v5[1].split('GY')
	GY = v6[0] 
	v7 = v6[1].split('GZ')
	GZ = v7[0] 

	v8 = v7[1].split('PL')
	PL = v8[0]
	v9 = v8[1].split('PR')
	PR = v9[0]

	v10 = v9[1].split('SL')
	SL = v10[0]
	v11 = v10[1].split('SR')
	SR = v11[0]

	em1 = SL
	em2 = SR
	ec1 = (105.4 * float(W) + 2 * float(V)) / (2 * 0.678181);	
	ec2 = (2 * float(V) - 105.4 * float(W)) / (2 * 0.678181);

	"""
	v8 = v7[1].split('UA')
	UA = v8[0]
	v9 = v8[1].split('UB')
	UB = v9[0]
	v10 = v9[1].split('UC')
	UC = v10[0]
	v11 = v10[1].split('UD')
	UD = v11[0]
	v12 = v11[1].split('UE')
	UE = v12[0]
	
	v13 = v12[1].split('IA')
	IA = v13[0]
	v14 = v13[1].split('IB')
	IB = v14[0]
	v15 = v14[1].split('IC')
	IC = v15[0]
	v16 = v15[1].split('ID')
	ID = v16[0]
	v17 = v16[1].split('IE')
	IE = v17[0]
	v18 = v17[1].split('IF')
	IF = v18[0]
	v19 = v18[1].split('IG')
	IG = v19[0]
	v20 = v19[1].split('IH')
	IH = v20[0]
	v21 = v20[1].split('II')
	II = v21[0]
	v22 = v21[1].split('IJ')
	IJ = v22[0]
	v23 = v22[1].split('IK')
	IK = v23[0]
	v24 = v23[1].split('IL')
	IL = v24[0]

	"""

	GX = str(float(GX) - bx)
	GY = str(float(GY) - by)
	GZ = str(float(GZ) - bz)

	sL = str(float(SL) * 0.678181)
	sR = str(float(SR) * 0.678181)

	vel = str((float(sL)+float(sR))/2)

	E1c.append(ec1)
	Time_val.append(t)
	print E1c
	print "\n"

 
	print "Time: " + str(t) + "sec\n" + "ec1: " + str(ec1) + "\n" + "ec2: " + str(ec2) + "\n" + "em1: " + str(em1) + "\n" + "em2: " + str(em2) + "\n" 

	print "================================================="
"""
	print "Time: " + Time + "\n" + "\nAccerleration on X: " + AX + "\nAccerleration on Y: " + AY + "\nAccerleration on Z: " + AZ + "\n" + "\nAngular rate (Gyroscope) on X: " + GX + "\nAngular rate (Gyroscope) on Y: " + GY + "\nAngular rate (Gyroscope) on Z: " + GZ + "\n" + "\nEncoder position left: " + PL + "\nEncoder position right: " + PR + "\nEncoder speed left: " + SL + "\nEncoder pspeed right: " + SR + "\nEncoder speed left (in mm/sec): " + sL + "\nEncoder pspeed right (in mm/sec): " + sR + "\nKhepera robot velocity: " + vel 
"""	

"""	
	+ "\nUltrasconic sensor 1: " + UA + "\nUltrasconic sensor 2: " + UB + "\nUltrasconic sensor 3: " + UC + "\nUltrasconic sensor 4: " + UD + "\nUltrasconic sensor 5: " + UE + "\n" + "\nInfrared sensor 1: " + IA + "\nInfrared sensor 2: " + IB + "\nInfrared sensor 3: " + IC + "\nInfrared sensor 4: " + ID + "\nInfrared sensor 5: " + IE + "\nInfrared sensor 6: " + IF + "\nInfrared sensor 7: " + IG + "\nInfrared sensor 8: " + IH + "\nInfrared sensor 9: " + II + "\nInfrared sensor 10: " + IJ + "\nInfrared sensor 11: " + IK + "\nInfrared sensor 12: " + IL
 
	
	print "================================================="
	
	#print x_Acc.split('x')[0];
	#print >>sys.stderr, 'X axis acceleration: "%lf"' % data1
	#print >>sys.stderr, 'X axis acceleration: "%d"' % data1
	#print >>sys.stderr, "X axis acceleration: %d" % data1+ "\n" +
"""
	
clientsocket1.send('0' + 'x' + '0')
plt.plot(Time_val, E1c) 
plt.xlabel('Time') 
plt.ylabel('E1c') 
plt.title('My first graph!') 
plt.show()



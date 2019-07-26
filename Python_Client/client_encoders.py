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

Ec1 = []
Em1 = []
Ec2 = []
Em2 = []
Time_val = []
t_old = 0.1
t_old_khepera = 0.1
F1 = []
F2 = []
while t_old < 80:
	time.sleep(0.05)
	end = time.time()
	t_new = end - start
	print 1/(t_new - t_old)
	F1.append(1/(t_new - t_old))
	t_old = t_new

	if t_old > 0 and t_old<=10:
		V = '350'
		W = '0'
	elif t_old>10 and t_old<=20:
		V='0'
		W= str(-3.1415/20)
	elif t_old>20 and t_old<=30:
		V='150'
		W= '0'
	elif t_old>30 and t_old<=40:
		V='0'
		W= str(-3.1415/20)
	elif t_old>40 and t_old<=50:
		V = '350'
		W = '0'
	elif t_old>50 and t_old<=60:
		V='0'
		W= str(-3.1415/20)
	elif t_old>60 and t_old<=70:
		V = '150'
		W = '0'
	elif t_old>70 and t_old<=80:
		V='0'
		W= str(-3.1415/20)


	clientsocket1.send(W + 'x' + V)
	data = clientsocket1.recv(4096)
	
	

	Time = data.split('T')[1]
	t_new_khepera = float(Time)
	print 1/(t_new_khepera - t_old_khepera)
	F2.append(1/(t_new_khepera - t_old_khepera))
	t_old_khepera = t_new_khepera

	SL = data.split('SL')[1]
	SR = data.split('SR')[1]

	em1 = SL
	em2 = SR
	ec1 = (105.4 * float(W) + 2 * float(V)) / (2 * 0.678181);	
	ec2 = (2 * float(V) - 105.4 * float(W)) / (2 * 0.678181);

	sL = str(float(SL) * 0.678181)
	sR = str(float(SR) * 0.678181)

	vel = str((float(sL)+float(sR))/2)

	Ec1.append(ec1)
	Em1.append(float(em1))
	Ec2.append(ec2)
	Em2.append(float(em2))
	Time_val.append(t_new)

	print "TimePython: " + str(t_new) + " sec \n"+  "TimeKhepera: " + str(Time) + " sec\n"+ "ec1: " + str(ec1) + "\n" + "ec2: " + str(ec2) + "\n" + "em1: " + str(em1) + "\n" + "em2: " + str(em2) + "\n" 
	print "================================================="
	
while True:
	W = '0'
	V = '0'
	clientsocket1.send(W + 'x' + V)
"""
plt.plot(Time_val, F1,'-b') 
plt.plot(Time_val, F2,'-r') 
plt.xlabel('Time') 
plt.ylabel('E1c') 
plt.title('My first graph!') 
plt.show()
while True:
	W = '0'
	V = '0'
	clientsocket1.send(W + 'x' + V)
"""
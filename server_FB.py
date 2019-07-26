import socket
import sys
import time
import math
import numpy as  np
import matplotlib.pyplot as plt 

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('192.168.1.142', 3000))
serversocket.listen(5) # become a server socket, maximum 5 connections
connection, address = serversocket.accept()

Time = '0.0'


#t = 0
Time_val_python = []
Time_val_khepera = []
t_old = 0.0
t_old_khepera = -1
python_freq = []
khepera_freq = []
i = 0

start = time.time()
t_new           = 0
t_old           = 0
t_old_khepera   = -1
count           = 1 
freq            = 20
tol             = 0.0001
delta           = 1/freq
#W               = '0'
#V               = '0'
v                = 0
W = []
V = []
SPDL = []
SPDR = []
vcommand = 0 
x = 0
y = 0
theta = 0

while (t_new <= 10.0):
    #time.sleep(0.01)
    

    end = time.time()
    t_new = end-start
    # print "Python time:" + str(t_new) + "\n"
   
    python_freq.append(1 / (t_new - t_old))
    Time_val_python.append(t_new)
    t_old = t_new

    
    data = connection.recv(4096)

        
    
    Time = data.split('T')[1]
    
    AX = data.split('AX')[1]
    AY = data.split('AY')[1]
    AZ = data.split('AZ')[1]
    
    GX = data.split('GX')[1]
    GY = data.split('GY')[1]
    GZ = data.split('GZ')[1]

    PL = data.split('PL')[1]
    PR = data.split('PR')[1]

    SL = data.split('SL')[1]
    SR = data.split('SR')[1]


    t_new_khepera = float(Time)
    SPDL.append(SL)
    SPDR.append(SR)

    # Encoder/motor speed in mm/sec
    spdL = float(SL) * 0.678181
    spdR = float(SR) * 0.678181
    velo = (spdL + spdR) / 2
    w    = (spdL - spdR) / 105.40
    t = t_new_khepera-t_old_khepera
    x = x + (t * velo * math.cos(theta + t * w / 2))
    y = y + (t * velo * math.sin(theta + t * w / 2))
    theta = theta + (t * w)
    sL = str(spdL)
    sR = str(spdR)
    vcommand = -1 * (x - 1000)
    VV = str(vcommand)
    WW = '0'
    connection.send(WW + 'x' + VV)

    #print "\nKhepera Time: " + Time + "\n"
    #print "\nAccerleration on X: " + AX + "\nAccerleration on Y: " + AY + "\nAccerleration on Z: " + AZ + "\n"  
    #print "\nAngular rate (Gyroscope) on X: " + GX + "\nAngular rate (Gyroscope) on Y: " + GY + "\nAngular rate (Gyroscope) on Z: " + GZ + "\n" 
    #print "\nEncoder position left: " + PL + "\nEncoder position right: " + PR + "\n"
    #print "\nEncoder speed left: " + SL + "\nEncoder pspeed right: " + SR + "\n" 
    #print "\nEncoder speed left (in mm/sec): " + sL + "\nEncoder pspeed right (in mm/sec): " + sR + "\n"
    #print "\nKhepera robot velocity: " + vel + "\n"
    
    khepera_freq.append(1 / (t_new_khepera - t_old_khepera))
    Time_val_khepera.append(t_new_khepera)   
    t_old_khepera = t_new_khepera

    
connection.send('0' + 'x' + '0')
serversocket.close()

for i in range(len(SPDL)):
    spdL = float(SPDL[i]) * 0.678181
    spdR = float(SPDR[i]) * 0.678181
    v = (spdL + spdR) / 2
    w = (spdL - spdR) / 105.40
    V.append(v)
    W.append(w)


khepera_freq.insert(20, 0)
Time_val_python.insert(0, 0)
Time_val_khepera.insert(0, 0)
V.insert(0, 0)
W.insert(0, 0)

X = []
X.insert(0, 0)
Y = []
Y.insert(0, 0)
THETA = []
THETA.insert(0, 0)


for i in range(1, len(V)):
    t = Time_val_khepera[i] - Time_val_khepera[i - 1]
    x = X[i - 1] + t * V[i - 1] * math.cos(THETA[i - 1] + t * W[i - 1] / 2)
    y = Y[i - 1] + t * V[i - 1] * math.sin(THETA[i - 1] + t * W[i - 1] / 2)
    th = THETA[i-1] + t * W[i - 1]
    X.append(x)
    Y.append(y)
    THETA.append(th)


plt.figure(1)
plt.subplot(6, 1, 1)
#plt.plot(Time_val_python, python_freq,'-r') 
plt.plot(Time_val_python, khepera_freq,'-b') 
plt.title('A tale of 6 subplots')
plt.ylabel('Khepera Frequency (Hz)')

plt.subplot(6, 1, 2)
plt.plot(Time_val_python, V,'-r') 
plt.ylabel('Velocity (mm/sec)')

plt.subplot(6, 1, 3)
plt.plot(Time_val_python, W,'-g') 
plt.ylabel('Angular (rad/sec)')

plt.subplot(6, 1, 4)
plt.plot(Time_val_python, X,'-c') 
plt.ylabel('X (mm)')

plt.subplot(6, 1, 5)
plt.plot(Time_val_python, Y,'-y') 
plt.ylabel('Y (mm)')

plt.subplot(6, 1, 6)
plt.plot(Time_val_python, THETA,'-k') 
plt.ylabel('theta (rad)')

plt.xlabel('Time') 

plt.figure(2)
x0 = X[0]
y0 = Y[0]
xend = X[-1]
yend = Y[-1]
plt.plot(X, Y,'-k') 
plt.plot(x0, y0,'*g') 
plt.plot(xend, yend,'*r') 

plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.grid()
plt.show()

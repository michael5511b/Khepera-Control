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
t_new           = -1
t_old           = 0
t_old_khepera   = -1
count           = 1 
freq            = 20
tol             = 0.0001
delta           = 1/freq
W               = '0'
V               = '0'

while (t_new <= 10.0):
    time.sleep(0.01)
    connection.send(W+'x'+V)  
    end = time.time()
    t_new = end-start
    # print "python time:" + str(t_new)
   
    python_freq.append(1/(t_new - t_old))
    Time_val_python.append(t_new)
    t_old = t_new

    
    data = connection.recv(4096)

    Time = data.split('T')[1]
    # print "K time: " + Time
    t_new_khepera = float(Time)
    print "t_new_khepera: " + str(t_new_khepera)
    print "t_old_khepera: " + str(t_old_khepera)
    print '\n'
    khepera_freq.append(1/(t_new_khepera - t_old_khepera))
    Time_val_khepera.append(t_new_khepera)   
    t_old_khepera = t_new_khepera

    
    
plt.plot(Time_val_python, python_freq,'-r') 
plt.plot(Time_val_python, khepera_freq,'-b') 
plt.xlabel('Time') 
plt.show()
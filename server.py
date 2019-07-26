import socket
import sys
import time
import math
import numpy as  np
import matplotlib.pyplot as plt 

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('192.168.1.142', 3000))
serversocket.listen(5) # become a server socket, maximum 5 connections


Time = '0.0'


#t = 0
Time_val_python = []
Time_val_khepera = []
t_old = 0.0
t_old_khepera = 0.0
python_freq = []
khepera_freq = []
i = 0

connection, address = serversocket.accept()
start = time.time()

t_old           = 0
t_old_khepera   = 0
count           = 1 
freq            = 20
tol             = 0.0001
delta           = 1/freq

while (t_old <= 10.0):

    # Khepera waits until a command sent from the python server, then continues
    W = '0'
    V = '0'
    end = time.time()
    t_new = end-start
    print "python time:" + str(t_new)
   
    if (abs(t_new - t_old)<delta):
        # connection.send(W+'x'+V)   
        # data = connection.recv(4096)

        
        python_freq.append(1/(t_new - t_old))
        Time_val_python.append(t_new)
        

        # print "K string: " + data
        # Time = data.split('T')[1]
        # print "K time: " + Time
        # data = ""
        # t_new_khepera = float(Time)
        # t_old_khepera = t_new_khepera
        count = count + 1   
    t_old = t_new
         

    
plt.plot(Time_val_python, python_freq,'-r') 
plt.xlabel('Time') 
plt.show()
"""
while True:
    W = '0'
    V = '0'
    serversocket.send(W + 'x' + V)
"""
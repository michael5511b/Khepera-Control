import socket
import sys
import time
import math
import numpy as  np
import matplotlib.pyplot as plt 


UDP_PORT_NO = 3000

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind(('192.168.1.142', UDP_PORT_NO))

while True:
    data, addr = serverSock.recvfrom(1024)
    print "Message: ", data

    print >>sys.stderr, 'received %s bytes from %s' % (len(data), addr)
    print >>sys.stderr, data


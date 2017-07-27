#!/usr/bin/env python

import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 6600
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

# Returns something like this: b'OK MPD 0.19.0\n'
data = s.recv(BUFFER_SIZE)  # type: bytes

if data.startswith(b'OK'):
    print("Connection succeed: ", data)

s.close()

#print("received data:", data)

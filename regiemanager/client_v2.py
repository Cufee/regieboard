import socket
import sys
import pickle


HOST = '127.0.0.1'
PORT = 6900
s = socket.socket()
s.connect((HOST, PORT))

while True:
    msg = {"This is a ": "test", "test": True}
    msg = pickle.dumps(msg)
    s.send(msg)
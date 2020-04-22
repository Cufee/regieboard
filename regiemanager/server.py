import socket
import time
import pickle

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 6900))

while True:
    msg = pickle.dumps({"action": "test"})
    msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + msg
    s.send(msg)



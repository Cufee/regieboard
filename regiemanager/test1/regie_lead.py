import socket, select, errno


#Setup
HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 6901

my_clientname = 'Regie Lead'
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

client_name = my_clientname.encode('utf-8')
client_header = f'{len(client_name):<HEADER_LENGTH}'.encode('utf-8')
client_socket.send(client_header + client_name)

while True:
    message = 
import sys
import socket
import pickle
import select


# Setup
HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 6900

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()


# Code
sockets_list = [server_socket]
clients = {}


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(
        sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            connection = receive_message(client_socket)
            if connection == False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = connection

            print(
                f'Accepted new connection from {client_address[0]}:{client_address[1]}\nClient name:{connection["data"].decode("utf-8")}')

        else:
            message = receive_message(notified_socket)

            if message is False:
                print(
                    f'Closed connection from {clients[notified_socket]["data"].decode("utf-8")}')
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            connection = clients[notified_socket]
            print(
                f'Received data from {connection["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(
                        connection["header"] + connection["data"] + message["header"] + message["data"])
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]

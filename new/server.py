import socket
from _thread import *

host = "127.0.0.1"
port = 1234

def client_handler(connection):
    connection.send(str.encode('You are now connected to the replay server...'))
    while True:
        data = connection.recv(2048)
        message = data.decode('utf-8')
        if message == 'BYE':
            break
        reply = f"Server: {message}"
        connection.sendall(str.encode(reply))
    connection.close()

def accept_connections(ServerSocket):
    Client, address = ServerSocket.accept()
    print(f'Connected to: {address[0]}:{str(address[1])}')
    start_new_thread(client_handler, (Client,))

def start_server(host, port):
    ServerSocket = socket.socket()
    try:
        ServerSocket.bind((host,port))
    except socket.error as e:
        print(str(e))
    print(f"Server is listening on the port {port}...")
    ServerSocket.listen()

    while True:
        accept_connections(ServerSocket)

start_server(host,port)
import socket
from _thread import *

host = "127.0.0.1"
port = 1234
clients = []
nicknames = []

def client_handler(connection):
    while True:
        data = connection.recv(2048)
        message = data.decode('utf-8')
        #if message == 'BYE':
        #     break
        #reply = f"Server: {message}"
        #connection.sendall(str.encode(reply))
        reply = f"Server: {message}"
        if message == "Bye":
            break
        for client in clients:
            if client == connection:
                continue
            else:
                client.send(str.encode(reply))
            

    connection.close()

def accept_connections(ServerSocket):
    Client, address = ServerSocket.accept()
    print(f'Connected to: {address[0]}:{str(address[1])}')

    clients.append(Client)
    nickname = Client.recv(1024)
    nicknames.append(nickname.decode('utf-8'))
    nick_message = f"Nickname set to: {nickname}".encode('utf-8')
    Client.send(nick_message)

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
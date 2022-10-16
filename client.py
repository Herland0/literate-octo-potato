import socket
host = '127.0.0.1'
port = 1234

ClientSocket = socket.socket()
print('Waiting for connection')
try:
    ClientSocket.connect((host,port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(2048)
while True:
    message = input('Your message: ')
    ClientSocket.send(str.encode(message))
    reply = ClientSocket.recv(2048)
    d_reply = reply.decode('utf-8')
    print(d_reply)
    if d_reply == 'BYE':
        break

ClientSocket.close()


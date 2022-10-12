import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

HOST = "127.0.0.1"
PORT = 65430

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST,PORT))
lsock.listen()

print(f"Listening on {(HOST, PORT)}")

lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data = None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None: 
                accept_wrapper(key.fileobj) #from listening socket need to accept connection
            else:
                service_connection(key, mask) #from client socket need to be serviced
except KeyboardInterrupt:
    print("Keyboard iterrupt, exiting")
finally:
    sel.clse()


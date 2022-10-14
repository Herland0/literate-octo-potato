import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    conn, addr = sock.accept() #ready to read 
    print(f"Accepted connection from {addr}")
    conn.setblocking(False) 
    data = types.SimpleNamespace(addr = addr, inb = b"", outb = b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE #bitwise OR to know if the client connection is ready for reading and writing
    sel.register(conn, events, data = data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb} to {data.addr}")
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


HOST = "127.0.0.1"
PORT = 65430

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defying socket
lsock.bind((HOST,PORT)) 
lsock.listen()

print(f"Listening on {(HOST, PORT)}")

lsock.setblocking(False) #socket in non blocking mode 
sel.register(lsock, selectors.EVENT_READ, data = None) #registers socket to be monitored with select - listening socket selectors.EVENT_READ

try:
    while True:
        events = sel.select(timeout=None) #returns key.fileobj is the socket obj, mask is an event mask for ready operations
        for key, mask in events:
            if key.data is None: 
                accept_wrapper(key.fileobj) #from listening socket need to accept connection
            else:
                service_connection(key, mask) #from client socket need to be serviced
except KeyboardInterrupt:
    print("Keyboard iterrupt, exiting")
finally:
    sel.clse()
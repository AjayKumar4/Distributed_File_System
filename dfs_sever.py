import socket
import threadpool
import time
import os

# global threadpool for server
server_thread_pool = threadpool.ThreadPool(500)

port_number = 8080

ip_address = socket.gethostbyname(socket.gethostname())

# create socket  and initialise to localhost:8000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = (ip_address, port_number)
print("starting up on %s port %s" % server_address)
# bind socket to server address and wait for incoming connections4
server.bind(server_address)
server.listen(1)
print(server.accept())
while True:
    # sock.accept returns a 2 element tuple
    connection, client_address = server.accept()
    print(server.accept())
    print("Connection from %s, %s\n" % connection, client_address)


print("Connection from %s, %s\n" % connection, client_address)
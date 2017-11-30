import socket
import threadpool
import time
import os

# this is a multithreaded client program that was used to test
# the server code

client_thread_pool = threadpool.ThreadPool(5)

ip_address = socket.gethostbyname(socket.gethostname())

port_num = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (ip_address, port_num)
print("connecting to %s on port %s\n" % server_address)
server.connect(server_address)


import socket
import threadpool
import time
import os

# function removes old items from cache
def auto_update_cache():
    global cache_queue
    while True:
        time.sleep(10)
        new_cache_queue = []
        for item in cache_queue:
            if item[2] < cache_time:
                new_cache_record = (item[0], item[1], item[2] + 1)
                new_cache_queue.append(new_cache_record)
        cache_queue = new_cache_queue

def get_server_response(socket):
    global response_var
    while True:
        data = socket.recv( 1024 )
        response_var = data
        if (data != None):
            # if reading cache item
            if(len(data.split("////")) == 2):
                split_data = data.split("////")
                add_to_cache(split_data[0], split_data[1])
                print(split_data[1])
            else:
                print(data)

# adds an item to the cache
def add_to_cache(path, contents):
    cache_queue.insert(0, (path, contents, 0))
    if len(cache_queue) > 5:
        cache_queue.pop()

# this is a multithreaded client program that was used to test
# the server code

client_thread_pool = threadpool.ThreadPool(5)

ip_address = socket.gethostbyname(socket.gethostname())

port_num = 8080


#each 1 is 10 seconds
cache_time = 2

# Stores last 5 accessed items
# (file_path, file_contents, age)
cache_queue = []

response_var = ""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (ip_address, port_num)
print("connecting to %s on port %s\n" % server_address)
server.connect(server_address)
client_thread_pool.add_task(
    get_server_response,
    server
)
client_thread_pool.add_task(
    auto_update_cache
)


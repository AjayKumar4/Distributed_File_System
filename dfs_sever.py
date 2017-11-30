import socket
import threadpool
import time
import os
import shutil
import datetime

class Client:
    # Initialise a new File System client
    def __init__(self, id, socket, path_to_root):
        self.id = id
        self.socket = socket
        self.dir_level = 0
        # Path to root is the path to the root of the file_system
        self.dir_path = [path_to_root]

    #
    # Testing functions
    #
    def log_member_data(self):
        print("")
        print("dir_path: " + (self.dir_path).__repr__())
        print("socket: " + (self.socket).__repr__())
        print("id: %d" % self.id)
        print("dir_level: %d" % self.dir_level)
        print("")


class FileSystemManager:

    # List for storing active clients
    active_clients = []

    # Next ID to be assigned to new client and events
    next_client_id = 0
    next_event_id = 0

    # List of events and IDs
    # ( event_id , command, time )
    events = []

    # List of the paths of currently locked files
    # ( client_id, time, path )
    locked_files = []

    # ThreadPool will contain threads managing the autorelease
    # of locks
    file_system_manager_threadpool = threadpool.ThreadPool(1)

    # Create new File System Manager and initialise the root
    def __init__(self, root_path):
        self.root_path = root_path
        #Add autorelease function to a new thread
        self.file_system_manager_threadpool.add_task(
            self.auto_release
        )

    # Generate a client ID and update next_client_id
    def gen_client_id(self):
        return_client_id = self.next_client_id
        self.next_client_id = self.next_client_id + 1
        return return_client_id

    # Generate a client ID and update next_event_id
    def gen_event_id(self):
        return_event_id = self.next_event_id
        self.next_event_id = self.next_event_id + 1
        return return_event_id

    #
    # Functions for interacting with clients
    #

    # Adds a new client to the file system manager
    # Returns the id of the client
    def add_client(self, connection):
        new_client_id = self.gen_client_id();
        new_client = Client(new_client_id, connection, self.root_path)
        self.active_clients.append(new_client)
        return new_client_id

def error_response(connection, error_code):
    response = ""
    if error_code == 0:
        response = "server error"
    if error_code == 1:
        response = "unrecognised command"
    connection.sendall(response)

def start_client_interaction(connection, client_address):
    try:
        #A client id is generated, that is associated with this client
        #client_id = file_system_manager.add_client(connection)
        client_id = FileSystemManager.add_client(connection)
        while True:
            data = connection.recv(1024)
            split_data = data.split()
            # Respond to the appropriate message
            if data == "KILL_SERVICE":
                # Kill service
                response = "Killing Service"
                connection.sendall("%s" % response)
                connection.close()
                os._exit(0)

            else:
                error_response(connection, 1)
    except:
        error_response(connection, 0)
        connection.close()

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
    server_thread_pool.add_task(
        start_client_interaction,
        connection,
        client_address
    )


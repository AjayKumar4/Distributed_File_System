import socket
import threadpool
import os
import sys
import dfs_server_filesystem_model
from dfs_server_filesystem_locking import lock, release
from dfs_server_filesystem_readwrite import read, write, delete
from dfs_server_filesystem_directory import cd, up, mkdir, rmdir, ls, pwd
from dfs_server_filesystem_errorexit import error_response, exit

# global threadpool for server
server_thread_pool = threadpool.ThreadPool(500)


# checks whether sufficient arguments have been provided
if len(sys.argv) != 3:
	print ("Correct usage: script, IP address, port number")
	exit()

# takes the first argument from command prompt as IP address
ip_address = str(sys.argv[1])

# takes second argument from command prompt as port number
port_number = int(sys.argv[2])

#port_number = 1024

#ip_address = socket.gethostbyname(socket.gethostname())

file_system_manager = dfs_server_filesystem_model.FileSystemManager('FileSystemDir')

def create_server_socket():
    # create socket  and initialise to localhost:8000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip_address, port_number)
    print("starting up on %s port %s" % server_address)
    # bind socket to server address and wait for incoming connections4
    sock.bind(server_address)
    sock.listen(1)

    while True:
        # sock.accept returns a 2 element tuple
        connection, client_address = sock.accept()
        print (client_address[0] + ":"+ str(client_address[1]) +" connected")
        # Hand the client interaction off to a seperate thread
        server_thread_pool.add_task(
            start_client_interaction,
            connection,
            client_address
        )

def start_client_interaction(connection, client_address):
    try:
        #A client id is generated, that is associated with this client
        client_id = file_system_manager.add_client(connection)
        while True:
            data = connection.recv(1024).decode()
            split_data = seperate_input_data(data)
            # Respond to the appropriate message
            if data == "KILL_SERVICE":
                kill_service(connection)
            elif split_data[0] == "ls":
                ls(connection, client_id, split_data, file_system_manager)
            elif split_data[0] == "cd":
                cd(connection, split_data, client_id,file_system_manager)
            elif split_data[0] == "up":
                up(connection, split_data, client_id,file_system_manager)
            elif split_data[0] == "read":
                read(connection, split_data, client_id,file_system_manager)
            elif split_data[0] == "write":
                write(connection, split_data, client_id,file_system_manager)
            elif split_data[0] == "delete":
                delete(connection, split_data, client_id,file_system_manager)
            elif split_data[0] == "lock":
                lock(connection, split_data, client_id,file_system_manager)
            elif split_data[0] == "release":
                release(connection, split_data, client_id,file_system_manager)
            elif split_data[0] == "mkdir":
                mkdir(connection, split_data, client_id,file_system_manager)
            elif split_data[0] == "rmdir":
                rmdir(connection, split_data, client_id,file_system_manager)
            elif split_data[0] == "pwd":
                pwd(connection, split_data, client_id, file_system_manager)
            elif split_data[0] == "exit":
                exit(connection, split_data, client_id, file_system_manager)
            else:
                error_response(connection, 1)
    except:
        error_response(connection, 0)
        connection.close()

def kill_service(connection):
    # Kill service
    #response = "Killing Service"
    #connection.sendall("%s" % response.encode())
    connection.close()
    os._exit(0)

#Function to split reveived data strings into its component elements
def seperate_input_data(input_data):
    seperated_data = input_data.split('////')
    return seperated_data



if __name__ == '__main__':
    create_server_socket()
    # wait for threads to complete
    server_thread_pool.wait_completion()
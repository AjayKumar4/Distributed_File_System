# Distributed_File_System

To run the Distributed_File_System, First need to Run dfs_server followed by dfs_client. The dfs_server and dfs_client code can be executed using an IDE such as PyCharm, or by performing in the terminal . dfs_client code can be executed multiple time in the different terminal.

To run the Server
python ./dfs_server.py

To run the Client
python ./dfs_client.py

There are a number of commands that can be run on the client that will have suitable responses returned by the server

ls - list files and directories in the current directory

ls directorypath - list files in specified directory

cd directorypath - move to specified directory

up - move up one directory

read filepath - read the contents of a file

write file_name - writes file from current directory on local machine to the current directory on the remote server

mkdir filename - make a directory at the following path

rmdir filename - delete a directory and its contents

lock filename - locks the specified file

release filename - releases a specified file

exit - exit the client

Following Features are implemented :

Distributed transparent file access
Directory Service
		The current position of each client is stored in their object on the server. There are functions that resolve paths
Caching (in the client)
		a list of recently viewed items is stored
		a thread is charged with making sure items are discarded after a set  period of time.
Locking
		Items being written to or deleted require a lock
		Locks are stored in a list on the server
		A thread has the task of checking that all of the locks have an 	owner who is active on the 		server. This process runs every minute.
Logging
		All events are logged on the server and can be viewed


threadpool.py file is downloaded from 
 http://code.activestate.com/recipes/577187-python-thread-pool/

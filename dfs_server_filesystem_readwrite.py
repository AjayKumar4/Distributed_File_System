#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 08 14:11:53 2017

@author: aj
"""

from dfs_server_filesystem_errorexit import error_response

def read(connection, split_data, client_id,file_system_manager):
    if len(split_data) == 2:
        response = file_system_manager.read_item(client_id, split_data[1])
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)

def write(connection, split_data, client_id,file_system_manager):
    response = ""
    if len(split_data) == 2:
        res = file_system_manager.write_item(client_id, split_data[1], "")
        if res == 0:
            response = "write successfull"
        elif res == 1:
            response = "file locked"
        elif res == 2:
            response = "cannot write to a directory file"
        connection.sendall(response.encode())
    elif len(split_data) == 3:
        res = file_system_manager.write_item(client_id, split_data[1], split_data[2])
        if res == 0:
            response = "write successfull"
        elif res == 1:
            response = "file locked"
        elif res == 2:
            response = "cannot write to a directory file"
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)

def delete(connection, split_data, client_id,file_system_manager):
    if len(split_data) == 2:
        res = file_system_manager.delete_file(client_id, split_data[1])
        response = ""
        if res == 0:
            response = "delete successfull"
        elif res == 1:
            response = "file locked"
        elif res == 2:
            response = "use rmdir to delete a directory"
        elif res == 3:
            response = "file doesn't exist"
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)
        

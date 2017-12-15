#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 08 14:11:53 2017

@author: aj
"""
from dfs_server_filesystem_errorexit import error_response

def lock(connection, split_data, client_id, file_system_manager):
    if len(split_data) == 2:
        client = file_system_manager.get_active_client(client_id)
        res = file_system_manager.lock_item(client, split_data[1])
        response = ""
        if res == 0:
            response = "file locked"
        elif res == 1:
            response = "file already locked"
        elif res == 2:
            response = "file doesn't exist"
        elif res == 3:
            response = "locking directories is not supported"
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)

def release(connection, split_data, client_id, file_system_manager):
    if len(split_data) == 2:
        client = file_system_manager.get_active_client(client_id)
        res = file_system_manager.release_item(client, split_data[1])
        if res == 0:
            response = split_data[1] + " released"
        elif res == -1:
            response = "you do not hold the lock for %s" % split_data[1]
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)
        

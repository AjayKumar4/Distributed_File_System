#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 08 14:11:53 2017

@author: aj
"""
from dfs_server_filesystem_errorexit import error_response

def cd(connection, split_data, client_id, file_system_manager):
    if len(split_data) == 2:
        res = file_system_manager.change_directory(split_data[1], client_id)
        response = ""
        if res == 0:
            response = "changed directory to %s" % split_data[1]
        elif res == 1:
            response = "directory %s doesn't exist" % split_data[1]
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)

def up(connection, split_data, client_id, file_system_manager):
    if len(split_data) == 1:
        file_system_manager.move_up_directory(client_id)
    else:
        error_response(connection, 1)

def mkdir(connection, split_data, client_id, file_system_manager):
    if len(split_data) == 2:
        response = ""
        res = file_system_manager.make_directory(client_id, split_data[1])
        if res == 0:
            response = "new directory %s created" % split_data[1]
        elif res == 1:
            response = "file of same name exists"
        elif res == 2:
            response = "directory of same name exists"
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)

def rmdir(connection, split_data, client_id, file_system_manager):
    if len(split_data) == 2:
        response = ""
        res = file_system_manager.remove_directory(client_id, split_data[1])
        if res == -1:
            response = "%s doesn't exist" % split_data[1]
        elif res == 0:
            response = "%s removed" % split_data[1]
        elif res == 1:
            response = "%s is a file" % split_data[1]
        elif res == 2:
            response = "directory has locked contents"
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)

def ls(connection, client_id, split_data, file_system_manager):
    response = ""
    if len(split_data) == 1:
        response = file_system_manager.list_directory_contents(client_id)
        connection.sendall(response.encode())
    elif len(split_data) == 2:
        response = file_system_manager.list_directory_contents(client_id, split_data[1])
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)


def pwd(connection, split_data, client_id, file_system_manager):
    if len(split_data) == 1:
        response = file_system_manager.get_working_dir(client_id)
        connection.sendall(response.encode())
    else:
        error_response(connection, 1)
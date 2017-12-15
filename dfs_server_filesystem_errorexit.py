#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 08 14:11:53 2017

@author: aj
"""

def exit(connection, split_data, client_id, file_system_manager):
    if len(split_data) == 1:
        file_system_manager.disconnect_client(connection, client_id)
    else:
        error_response(connection, 1)

def error_response(connection, error_code):
    response = ""
    if error_code == 0:
        response = "server error"
    if error_code == 1:
        response = "unrecognised command"
    connection.sendall(response.encode())
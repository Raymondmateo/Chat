"""
    Author:            Jake Casey, Jevaughn Stewart, Raymond Mateo
    Creation Date:     Nov. 24, 2023
    Due Date:          Dec. 14, 2023
    Course:            CSC 328 010
    Professor Name:    Dr. Schwesinger
    Assignment:        Chat Server
    Filename:          lib.py
    Purpose:           The library is used for certain functions.
"""
import json
import threading
import sys
import socket
import struct
import time
import os
import logging

"""
Function Name:  close_socket
Parameters:     word: The word to be serialized.
Returns:        combined_data - Combined binary data
"""
def gen_word_packet(word):
    try:
        json_data = json.dumps(word)
        combined_data = len(json_data).to_bytes(2, byteorder='big') + json_data.encode('utf-8')
        return combined_data
    except Exception as e:
        print(f"An error occurred: {e}")

"""
Function Name:  close_socket
Parameters:     sock - the socket being closed.
Returns:        none
"""
def close_socket(sock):
    try:
        sock.close()
    except Exception as e:
        print(f"Error closing socket: {e}")

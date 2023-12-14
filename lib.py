import json
import threading
import sys
import socket
import struct
import time
import os
import logging

"""
Generate a packet containing a serialized JSON word.

Parameters:
- word: The word to be serialized.

Returns:
Combined binary data.
"""
def gen_word_packet(word):
    try:
        json_data = json.dumps(word)
        combined_data = len(json_data).to_bytes(2, byteorder='big') + json_data.encode('utf-8')
        return combined_data
    except Exception as e:
        print(f"An error occurred: {e}")

def close_socket(sock):
    try:
        sock.close()
    except Exception as e:
        print(f"Error closing socket: {e}")

#!/usr/bin/env python3
# import subprocess
import sys
import socket
import struct
import threading
import json
from textView import InputApp

messages = []
app_lock = threading.Lock()

messages_lock = threading.Lock()
proc_stdout = sys.stdout


def display_messages(messages, app):
    while True:
        pass


def gen_word_packet(word):
    try:
        word_bytes = word.encode('utf-8')
        pkt_len = len(word_bytes)
        len_bytes = struct.pack('>H', pkt_len)
    except Exception as e:
        print(f"An error occurred: {e}")
    return len_bytes + word_bytes


def receive_thread(sock, app):
    try:
        while True:
            combined_data = sock.recv(4096)
            if not combined_data:
                print("NO message")
                break
          # You might need to adjust the buffer size
            data_length = int.from_bytes(combined_data[:4], byteorder='big')
            json_data = combined_data[4:4+data_length].decode('utf-8')
        # Deserialize the JSON data back into a tuple
            received_tuple = tuple(json.loads(json_data))
            with messages_lock and app_lock:
                messages.append(received_tuple[0])
                app.append_message(received_tuple[0])
                # display_message(received_tuple)

                print(f"Received word: {received_tuple}")
    except Exception as e:
        print(f"Error receiving word packet: {e}")
        return None


def run_client(server_address, server_port):
    try:
        with open('logs.txt', 'w') as file:
            sys.stdout = file
            c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c_sock.connect((server_address, server_port))
            print(f"Connected to server at {server_address}:{server_port}")
            app = InputApp(c_sock)
            run_thread = threading.Thread(
                target=receive_thread, args=(c_sock, app,))
            run_thread.start()
           # message = gen_word_packet("Hello Server")
           # c_sock.sendall(message)
            app.run()

            run_thread.join()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        c_sock.close()
        print("Client socket closed.")
        file.close()
        proc_stdout.write('\033c')
        proc_stdout.flush()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./client.py <server_address> <server_port>")
        sys.exit(1)

    server_address = sys.argv[1]
    try:
        server_port = int(sys.argv[2])
        if not (10000 < server_port < 65535):
            raise ValueError("Port should be between 10000 and 65535.")
    except ValueError:
        print("Invalid port number. Please provide a valid port between 10000 a\
nd 65535.")
        sys.exit(1)

    run_client(server_address, server_port)
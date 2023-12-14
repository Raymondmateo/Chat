#!/usr/bin/env python3
import sys
import socket
import random
import struct
import time
import threading
import json
clients_lock = threading.Lock()
buff_lock = threading.Lock()
clients = []
words = [("my", "csdcsdcsd", 3.11), ("cdssd", 23, 2.33)]
buff = []

temp = 0


def send_messages(message):
    temp = (message, "wooowoww", 2.22)
    word_pkt = gen_word_packet(temp)
    with clients_lock:
        for client in clients:
            client.sendall(word_pkt)


def go(client):
    while True:
        len_bytes = client.recv(2)
        if not len_bytes:
            clients.remove(client)
            print(f"Connection closed by {client.getpeername()}")
            break
        pkt_len = struct.unpack('>H', len_bytes)[0]
        received_data = client.recv(pkt_len).decode('utf-8')
        print("got here")
        send_thread = threading.Thread(
            target=send_messages, args=(received_data,))
        send_thread.start()
        with buff_lock:
            buff.append(received_data)
            print(f"Received message: {buff}")


def receive_messages(client):
    try:
        run_thread = threading.Thread(target=go, args=(client,))
        run_thread.start()

    except Exception as e:
        print(f"Error receiving message: {e}")


def gen_word_packet(word):
    try:
        json_data = json.dumps(word)
        combined_data = len(json_data).to_bytes(
            4, byteorder='big') + json_data.encode('utf-8')
    except Exception as e:
        print(f"An error occurred: {e}")
    return combined_data


def accept_clients(s_sock):
    try:
        while True:
            client, addr = s_sock.accept()
            with clients_lock:
                if client:
                    clients.append(client)
                    receive_messages(client)
                    print(f"Accepted connection from {addr}")
    except KeyboardInterrupt:
        print("\nServer was interrupted. Closing server socket...")
    except Exception as e:
        print(f"Error receiving message: {e}")
    finally:
        with clients_lock:
            for elt in clients:
                elt.close()
                clients.remove(elt)
        s_sock.close()
        print("Server socket closed.")
        sys.exit(1)
        # Start a new thread to receive messages from the client


def run_server(port):
    try:
        s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_sock.bind(("0.0.0.0", port))
        s_sock.listen(5)
        print(f"Server is listening on port {port}...")

        accept_thread = threading.Thread(target=accept_clients, args=(s_sock,))
        accept_thread.start()

        accept_thread.join()

        # Wait for the accept thread to finish (this will never happen in this example
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./server <port>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        if not (10000 < port < 65535):
            raise ValueError("Port should be between 10000 and 65535.")
    except ValueError:
        print("Invalid port number. Please provide a valid port between 10000 and 65535.")
        sys.exit(1)
    run_server(port)

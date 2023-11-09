# Handshake codes:
# ICON: Initial CONnection
# RACK: ACKnowledge received Request
# PACK: ACKnowledge received Payload
# DONE: last message before disconnect

import socket
import os, sys
import time

import json
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

from lib import packets
from lib import database

HOST = "127.0.0.1"
PORT = 65432 # Most ports 1023 - 65535 should work.

# packet for initial connection

os.system("cls") # clears the console
# Create a new socket using IPv4 (AF_INET) and TCP protocol (SOCK_STREAM).
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    # Bind the socket to the specified HOST and PORT.
    server.bind((HOST, PORT))
    # Enable the server to accept connections. By default, it does not limit the number of queued connections.
    server.listen()
    # Wait until a client connects, then return a new socket (conn) and the client's address.
    while True:
        conn, addr = server.accept()
        # Use the new socket (conn) to communicate with the connected client.
        with conn:

            print(f"Connected by {addr}")
            
            # Keep receiving data from the client until it disconnects.
            packet = conn.recv(256) # receives ICON
            print("Packet: " + str(packet))
            
            # Check that the first packet received is an ICON packet.
            decoded_packet = packets.Packet.fromBytes(packet)
            if (decoded_packet[2] == "ICON"):
                conn.sendall(packet)
            else:
                conn.sendall("huh".encode('utf-8'))
                print("Packet is not an ICON packet.")
                
            
        # Loop here waiting for data
        while False:
            # Receive up to 1024 bytes of data from the client.
            data = conn.recv(2**13)
            
            # If no data was received, the client is idle.
            if not packet:
                break
            
            # Send ACK here instead of full packet
            conn.sendall("DONE".encode('utf-8'))
            # format the data
            formatted_data = str(data.decode('utf-8')).split("\n")
            # create a dictionary for each client
            

            # # get the database
            #         database = []
            #         with open('database/database.json', 'r') as file:
            #             database = json.load(file)
# Handshake codes:
# ICON: Initial CONnection
# REQD: REQuest Data
# PACK: ACKnowledge received Payload

# Potential, but haven't used in code yet:
# RACK: ACKnowledge received Request
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
            # print(f"Connected by {addr}")
            
            # 1) Wait for and receive ICON
            packet = conn.recv(256)
            if packet: # makes sure the packet isn't empty
                print("Packet: " + str(packet))
                
                # 2, 3) Check that the first packet received is an ICON packet.
                decoded_packet = packets.Packet.fromBytes(packet)
                if (decoded_packet[2] == "ICON"):
                    conn.sendall(packet)
                else:
                    WHAT = packets.Packet("WHAT", "", "")
                    conn.sendall(packets.Packet.toBytes(WHAT))
                    print("Packet received from client was not an ICON packet.")
            
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
# Handshake codes:
# ICON: Initial CONnection
# RACK: ACKnowledge received Request
# PACK: ACKnowledge received Payload
# DONE: last message before disconnect

import socket
import os, sys

import json
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

from lib import packets
from lib import database

HOST = "127.0.0.1"
PORT = 65432 # Most ports 1023 - 65535 should work.

os.system("cls") # clears the console
# Create a new socket using IPv4 (AF_INET) and TCP protocol (SOCK_STREAM).
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    # Bind the socket to the specified HOST and PORT.
    server.bind((HOST, PORT))
    # Enable the server to accept connections. By default, it does not limit the number of queued connections.
    server.listen()
    # Wait until a client connects, then return a new socket (conn) and the client's address.
    conn, addr = server.accept()
    # Use the new socket (conn) to communicate with the connected client.
    with conn:

        ######### DATABASE TEST #########

        # getter test
        db = database.Database()
        users = db.getUsers()
        plants = db.getPlants()

        client_id = db.getClientId("dev")

        userData = db.getUserData(client_id)
        balance = db.getBalance(client_id)
        userPlants = db.getUserPlants(client_id)
        singleUserPlant = db.getSingleUserPlant(client_id, "")

        print(f"Users: \n{users}\n")
        print(f"Plants: \n{plants}\n\n")

        print(f"Client ID: \n{client_id}\n\n")

        print(f"User Data: \n{userData}\n\n")
        print(f"Balance: \n{balance}\n\n")
        print(f"User Plants: \n{userPlants}\n\n")
        print(f"Single User Plant: \n{singleUserPlant}\n\n")
        # end getter test


        ######### END DATABASE TEST #########

        print(f"Connected by {addr}")
        # get the database
        database = []
        with open('database/database.json', 'r') as file:
            database = json.load(file)
        # Keep receiving data from the client until it disconnects.
        data = conn.recv(1024)
        conn.sendall("ICON".encode('utf-8'))
        # Loop here waiting for data
        while True:
            # Receive up to 1024 bytes of data from the client.
            data = conn.recv(1024)
            
            # If no data was received, the client is idle.
            if not data:
                break
            
            # Send ACK here instead of full packet
            conn.sendall("DONE")
            # format the data
            formatted_data = str(data.decode('utf-8')).split("\n")
            # create a dictionary for each client
            
                
            # update database with the newly recieved data
            with open('database/database.json', 'a') as json_file:
                json.dump(database, json_file, indent=4)
            

import socket
import os, sys

import json

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

from lib import packets

HOST = "127.0.0.1"
PORT = 65432 # Most ports 1023 - 65535 should work.

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
        print(f"Connected by {addr}")
        # get the database
        database = []
        # Keep receiving data from the client until it disconnects.
        while True:
            # Receive up to 1024 bytes of data from the client.
            data = conn.recv(1024)
            # If no data was received, the client has disconnected.
            if not data:
                break
            # Send the received data back to the client (echo).
            # Send ACK here instead of full packet? yes. ACK packet_id
            conn.sendall(data)
            # format the data
            formatted_data = str(data.decode('utf-8')).split("\n")
            # create a dictionary for each client
            for clientData in formatted_data:
                # clients info
                client_id = clientData[0:8]
                ip = clientData[8:16]
                packet_id = clientData[16:24]
                data = clientData[32:]
                # create a dictionary to send to the database
                data_dict = {"client_id": client_id, "ip": ip, "packet_id": packet_id, "data": data}
                database.append(data_dict)

            with open('database/database.json', 'a') as json_file:
                json.dump(database, json_file, indent=4)
            # update database with the newly recieved data

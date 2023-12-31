# Handshake codes:
# ICON: Initial CONnection
# REQD: REQuest Data
# DATA: Data
# DACK: ACKnowledge received Data
# DONE: last message before disconnect

import socket
import threading
import os, sys
import time

import json
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

from lib import packets
from lib import database

HOST = "0.0.0.0" # opens on all network devices on computer
PORT = 65432 # Most ports 1023 - 65535 should work.

db = database.Database()

# each connection calls this
def handle_client(conn, addr):
    print(f"Connected to {addr}")
    with conn:
        while True:
            try:
                # Wait for and receive ICON
                packet = conn.recv(2048)
                if packet: # makes sure the packet isn't empty
                    # print("Packet: " + str(packet))
                    
                    # Check that the first packet received is an ICON packet.
                    decoded_packet = packets.Packet.fromBytes(packet)
                    if (decoded_packet[2] == "ICON"):
                        conn.sendall(packet)
                        print("RECV | ICON | Sending copy back...")
                    elif (decoded_packet[2] == "REQD"): # data request packet
                        if (decoded_packet[4] == "USER"):
                            print("RECV | REQD | Sending data...")
                            username = decoded_packet[3].replace("\x00", "")
                            if not db.getUserData(username):
                                # Create new user profile
                                db.createNewUser(username)
                            
                            data_packet = packets.Packet("DATA", "SERVER", json.dumps(db.getUserData(username)))
                            conn.sendall(packets.Packet.toBytes(data_packet))
                            print("SEND | DATA | " + str(data_packet))
                        if (decoded_packet[4] == "PLANTS"):
                            print("RECV | REQD | Sending data...")
                            username = decoded_packet[3].replace("\x00", "")
                            data_packet = packets.Packet("DATA", "SERVER", json.dumps(db.getPlants()))
                            conn.sendall(packets.Packet.toBytes(data_packet))
                            print("SEND | DATA | " + str(data_packet))
                        
                    elif (decoded_packet[2] == "DATA"): # packet containing data (to store in database)
                        index = -1
                        print("RECV | DATA | Copying to database...")
                        username = decoded_packet[3].replace("\x00", "")
                        with open('database/database.json') as f:
                            pydata = json.load(f)
                            for i, user in enumerate(pydata["users"]):
                                if user["username"] == username:
                                    index = i
                        f.close()
                        
                        with open('database/database.json') as f:
                            jsondata = json.load(f)
                        f.close()
                        
                        print("\n" + decoded_packet[4])
                        print(type(decoded_packet[4]))
                        jsondata['users'][index]['user_data'] = json.loads(decoded_packet[4])
                        
                        with open('database/database.json', 'w') as f:
                            json.dump(jsondata, f)
                        f.close()
                        
                        # send back data acknowledgement packet to client
                        DACK = packets.Packet("DACK", "SERVER", "")
                        conn.sendall(packets.Packet.toBytes(DACK))
                        print("SEND | DACK")
                    
                    # DONE packet confirmation
                    elif (decoded_packet[2] == "DONE"):
                        print("RECV | DONE | Username: " + str(decoded_packet[3]))
                        
                    elif (decoded_packet[2] == "WHAT"):
                        conn.sendall(packets.Packet.toBytes(packets.Packet("", "", ""))) #TODO send previous packet
                        print("RECV | WHAT | Sending previous packet again...")
                    else:
                        pass
                else:
                    pass
            except socket.error as oops:
                # print("ERR  | " + oops)
                pass
            finally:
                pass

def start_server(HOST, PORT):
    # open a TCP socket 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT)) # bind to the given host ip and port
        server.listen() # listen for connections
        print("Server is listening on", HOST, PORT)
        while True:
            conn, addr = server.accept() # accept incoming connections
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start() # start a thread for each client as to allow multiple connections
            print(f"Active connections: {threading.active_count() - 1}")

HOST = "0.0.0.0"
PORT = 65432 # Most ports 1023 - 65535 should work.
os.system("cls") # clears the console
start_server(HOST, PORT)
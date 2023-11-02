import socket
import os, sys

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

from lib import packets

HOST = "127.0.0.1"
PORT = 65432 # This needs to match the server's port.

# Create a new socket using IPv4 (AF_INET) and TCP protocol (SOCK_STREAM).
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Establish a connection to the specified server (HOST and PORT).
    s.connect((HOST, PORT))
    # Send a byte-string message "ICON" to the server.
    s.sendall("ICON".toBytes())
    # Wait for a response from the server and receive up to 1024 bytes of data.
    data = s.recv(1024)

# Print the data received from the server.
formatted_data = str(data.decode('utf-8')).split("\n")
for i in formatted_data:
    if len(i) > 24:
        packets.Packet.summary(i)
        
# To wrap up...
# Client sends "DONE {modified_dictionary}" 
# Server receives it, tries to modify the database.
#   if failure, send "BAD" or something
#   if success, send "DONE"
# client closes connections


# To send data...
# s.sendall(packet_to_send.toBytes()) 
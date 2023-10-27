import socket
import os, sys

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

from lib import packets

HOST = "127.0.0.1"
PORT = 65432 # This needs to match the server's port.

test_packet_a = packets.Packet(4, HOST, 5, "update_water(16)")
test_packet_b = packets.Packet(4, HOST, 6, "update_food(5)")
test_packet_c = packets.Packet(4, HOST, 7, "user_theme(\"dark\")")
test_packet_d = packets.Packet(4, HOST, 8, "user_add_plant(USER_ID, PLANT_NAME, COST)")

test_packets = [test_packet_a, test_packet_b, test_packet_c, test_packet_d]

# Create a new socket using IPv4 (AF_INET) and TCP protocol (SOCK_STREAM).
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Establish a connection to the specified server (HOST and PORT).
    s.connect((HOST, PORT))
    # Send a byte-string message "Hello, world" to the server. (legacy comment)
    for test_packet in test_packets:
        s.sendall(test_packet.toBytes())
    # Wait for a response from the server and receive up to 1024 bytes of data.
    data = s.recv(1024)

# Print the data received from the server.
formatted_data = str(data.decode('utf-8')).split("\n")
for i in formatted_data:
    if len(i) > 24:
        packets.Packet.summary(i)
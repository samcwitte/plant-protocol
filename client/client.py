import socket

HOST = "127.0.0.1"
PORT = 65432 # This needs to match the server's port.

# Create a new socket using IPv4 (AF_INET) and TCP protocol (SOCK_STREAM).
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Establish a connection to the specified server (HOST and PORT).
    s.connect((HOST, PORT))
    # Send a byte-string message "Hello, world" to the server.
    s.sendall(b"Hello, world")
    # Wait for a response from the server and receive up to 1024 bytes of data.
    data = s.recv(1024)

# Print the data received from the server.
print(f"Received {data!r}")
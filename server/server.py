import socket

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
        # Keep receiving data from the client until it disconnects.
        while True:
            # Receive up to 1024 bytes of data from the client.
            data = conn.recv(1024)
            # If no data was received, the client has disconnected.
            if not data:
                break
            # Send the received data back to the client (echo).
            conn.sendall(data)

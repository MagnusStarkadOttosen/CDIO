import socket
import sys

from src.server.command_processor import process_command

# Set up the server
server_address = ('', 10000)
buffer_size = 1024

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket
sock.bind(server_address)
sock.listen(1)

print("EV3 Server listening for commands...")

try:
    # Wait for a connection
    connection, client_address = sock.accept()
    print("Connection from", client_address)
    while True:
        data = connection.recv(buffer_size)
        if data:
            command = data.decode('utf-8').strip()
            print("Received command:", command)
            if command == "exit":
                break
            process_command(command)
            connection.sendall("OK".encode('utf-8'))
finally:
    print("Exiting server.")
    connection.close()
    print("Connection closed.")
    sock.close()
    print("Socket closed.")

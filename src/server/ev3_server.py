import socket
import sys

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
    print ("Connection from", client_address)

    while True:
        data = connection.recv(buffer_size)
        if data:
            command = data.decode('utf-8').strip()
            print ("Received command:", command)

            if command == "exit":
                print ("Exiting server.")
                break
            elif command == "forward ":
                print ("Moving forward" ) # Placeholder
            else:
                print ("Unknown command:", command)
        else:
            break
finally:
    connection.close()
    sock.close()
import socket
import sys

# Set up the connection
ev3_address = ('ev3dev', 10000) 
buffer_size = 1024

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(ev3_address)
    print("Connected to EV3. Type 'exit' to quit.")

    while True:
        command = input("Enter command: ")
        if command:
            sock.sendall(command.encode('utf-8'))

            if command == "exit":
                break
        else:
            print("Please enter a command.")
finally:
    print("Closing connection.")
    sock.close()
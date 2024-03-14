import socket
import sys

# Set up the connection
# ev3_address = ('ev3dev', 10000)
ev3_address = ('127.0.0.1', 10000)
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
except socket.gaierror as e:
    print(f"Error connecting to EV3: {e}")
finally:
    print("Closing connection.")
    sock.close()

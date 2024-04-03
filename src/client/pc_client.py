import socket
import cv2
import numpy as np
from src.vision.shape_detection import Shapes


# Set up the connection
# ev3_address = ('ev3dev', 10000)
ev3_address = ('127.0.0.1', 10000)
buffer_size = 1024

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(ev3_address)
    print("Connected to EV3. Type 'exit' to quit.")
    test_commands = ["rotate 180", "rotate -90", "exit"]
    for command in test_commands:
        if(command):
            sock.sendall(command.encode('utf-8'))
            print(f"Sent: {command}")
            server_response = sock.recv(buffer_size)
        else:
            print("test")
   
except socket.gaierror as e:
    print(f"Error connecting to EV3: {e}")
finally:
    print("Closing connection.")
    sock.close()

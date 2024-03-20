import socket
import cv2
import numpy as np
from src.vision.shape_detection import Shapes

from src.client.pathFinder import findNearestBall, balls_are_remaining
# Set up the connection
# ev3_address = ('ev3dev', 10000)
ev3_address = ('127.0.0.1', 10000)
buffer_size = 1024

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(ev3_address)
    print("Connected to EV3. Type 'exit' to quit.")
    """balls_remain = True
    while balls_remain:
        image = cv2.imread('images/3.jpg')
        shapes = Shapes(image)
        shapes.detect_balls()
        balls_remain = balls_are_remaining(shapes)
        if not balls_remain:
            command = "exit"
        else:
            nearest = findNearestBall(np.array([7, 9], dtype=int), shapes)
            # WHEN DETECT ROBOT FUNCTION DONE, SWITCH OUT HARD CODED ROBOT POSITION
            if not nearest == 0:
                x = nearest.x
                y = nearest.y
                d = nearest.d
                command = f"move {d}"
                print(command)
                # command = input("Enter command: ")
                if command:
                    sock.sendall(command.encode('utf-8'))
                    break # TEMP FOR TESTING
                if command == "exit":
                    break
                else:
                    print("Please enter a command.")
    print("Connected to EV3.")"""
    test_commands = ["move 20"]
    for command in test_commands:
        sock.sendall(command.encode('utf-8'))
        print(f"Sent: {command}")
        server_response = sock.recv(buffer_size)
except socket.gaierror as e:
    print(f"Error connecting to EV3: {e}")
finally:
    print("Closing connection.")
    sock.close()

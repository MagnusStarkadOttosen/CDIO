import socket
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D, SpeedPercent
# from src.server.command_processor import CommandProcessor

# cp = CommandProcessor()

# Set up the server
server_address = ('', 10000)
# server_address = ('127.0.0.1', 10000)
buffer_size = 1024

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket
sock.bind(server_address)
sock.listen(1)

print("EV3 Server listening for commands...")

try:
    tank_drive = MoveTank
    tank_drive.on_for_degrees(SpeedPercent(30), SpeedPercent(30), 100)
    tank_drive.stop()
    # Wait for a connection
    connection, client_address = sock.accept()
    print("Connection from", client_address)

    while True:

        data = connection.recv(buffer_size)
        if data:
            command = data.decode('utf-8').strip()
            # cp.process_command(command)
            print("Received command:", command)

            """if command == "exit":
                print("Exiting server.")
                break
            elif command == "forward":
                print ("Moving forward" ) # Placeholder
            else:
                print ("Unknown command:", command)"""
        else:
            break
finally:
    connection.close()
    sock.close()

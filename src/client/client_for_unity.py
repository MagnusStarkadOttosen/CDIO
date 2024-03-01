import socket

# Set up the connection
unity_address = ('127.0.0.1', 8052) 
buffer_size = 1024

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(unity_address)
    print("Connected to Unity. Type 'exit' to quit.")

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
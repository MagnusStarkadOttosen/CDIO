import socket

# Set up the connection
ev3_address = ('ev3dev', 10000)
#ev3_address = ('127.0.0.1', 10000)
buffer_size = 1024


class ClientPC:
    def __init__(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(ev3_address)
            print("Connected to EV3.")

        except socket.gaierror as e:
            print(f"Error connecting to EV3: {e}")

    def close_connection(self):
        print("Closing connection.")
        self.sock.close()

    def send_command(self, command):
        try:
            if command:
                self.sock.sendall(command.encode('utf-8'))
                print(f"Sent: {command}")
                self.sock.recv(buffer_size)
                if command == 'exit':
                    self.close_connection()
            else:
                print("test")
        except (ConnectionError, TimeoutError, BrokenPipeError, OSError) as e:
            print(f"Error during socket operation: {e}")

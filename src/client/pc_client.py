import socket

# Set up the connection
ev3_address = ('ev3dev', 10000)
#ev3_address = ('127.0.0.1', 10000)
buffer_size = 1024


class ClientPC:
    """
    A class to manage TCP/IP communication with an EV3 device.
    """
    def __init__(self):
        """
        Initializes the ClientPC object, sets up a TCP/IP socket, and attempts to connect to the EV3 device.
        """
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(ev3_address)
            print("Connected to EV3.")

        except socket.gaierror as e:
            print(f"Error connecting to EV3: {e}")

    def close_connection(self):
        """
        Closes the TCP/IP connection to the EV3 device.
        """
        print("Closing connection.")
        self.sock.close()

    def send_command(self, command):
        """
        Sends a command to the EV3 device.

        Parameters
        ----------
        command : str
            The command to be sent to the EV3 device.

        Raises
        ------
        ConnectionError, TimeoutError, BrokenPipeError, OSError
            If an error occurs during the socket operation.
        """
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

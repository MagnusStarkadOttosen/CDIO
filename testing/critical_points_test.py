# Import necessary libraries and functions
from src.client.field.deliver_point import deliver_points
from src.client.pc_client import ClientPC

# Setup your robot's client interface
client_pc = ClientPC()

# Define the target point where the robot should deliver the ball
target_point = (300, 600)

# Call the deliver_points function
try:
    deliver_points(target_point)
    print("Delivery process started successfully.")
except Exception as e:
    print(f"An error occurred during the delivery process: {str(e)}")

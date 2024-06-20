# Import necessary libraries and functions
from src.client.field.collect_from_corner import is_ball_in_corner
from src.client.pc_client import ClientPC
from src.client.vision.camera import initialize_camera

# Setup your robot's client interface
print("test321")
client_pc = ClientPC()
print("test123")
# Define the target point where the robot should deliver the ball
target_point = (300, 600)
camera = initialize_camera(index=2)
# Call the deliver_points function
try:
    is_ball_in_corner(client_pc, target_point, camera)
    print("Delivery process started successfully.")
except Exception as e:
    print(f"An error occurred during the delivery process: {str(e)}")

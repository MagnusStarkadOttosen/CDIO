# Import necessary libraries and functions
from src.client.field.collect_from_corner import collect_from_corner
from src.client.pc_client import ClientPC
from src.client.vision.camera import initialize_camera
from src.client.vision.shape_detection import detect_robot

# Setup your robot's client interface
print("test321")
client_pc = ClientPC()
print("test123")
# Define the target point where the robot should deliver the ball
target_point = (300, 600)
camera = initialize_camera(index=2)
# Call the deliver_points function
try:
    collect_from_corner(client_pc, target_point, camera)
    print("Delivery process started successfully.")
except Exception as e:
    print(f"An error occurred during the delivery process: {str(e)}")

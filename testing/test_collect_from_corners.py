from src.client.field.collect_from_corner import robot_movement_based_on_corners, check_corners
from src.client.pc_client import ClientPC
from src.client.vision.camera import initialize_camera

print("Test collecting from corners.")
client_pc = ClientPC()


CORNERS = [(0, 0), (0, 1200), (1800, 0), (1800, 1200)]
PIVOT_POINTS = [(300, 600), (1500, 600)]
IMAGE_SIZE = [1200, 1800]
ball_coords = (1790, 10, 5)

try:
    corner_results = check_corners(ball_coords)
    robot_movement_based_on_corners(corner_results)
    print("Delivery process started successfully.")
except Exception as e:
    print(f"An error occurred during the delivery process: {str(e)}")
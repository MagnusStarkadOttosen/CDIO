from src.client.field.collect_from_corner import collect_from_corner, get_ball_coordinates, \
    robot_action_based_on_corners
from src.client.pc_client import ClientPC
from src.client.vision.camera import initialize_camera

print("Test collecting from corners.")
client_pc = ClientPC()
camera = initialize_camera(index=2)

CORNERS = [(0, 0), (0, 1200), (1800, 0), (1800, 1200)]
PIVOT_POINTS = [(300, 600), (1500, 600)]
IMAGE_SIZE = [1200,1800]
corner_result = get_ball_coordinates(camera,corner_threshold=50)

try:
    robot_action_based_on_corners(corner_result, client_pc, PIVOT_POINTS)
    print("Delivery process started successfully.")
except Exception as e:
    print(f"An error occurred during the delivery process: {str(e)}")

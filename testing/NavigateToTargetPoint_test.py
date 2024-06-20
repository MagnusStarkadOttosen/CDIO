import cv2
import numpy as np
from src.client.field.coordinate_system import are_points_close, find_corner_points_full, warp_perspective
from src.client.pathfinding.CalculateCommandList import rotate_vector_to_point
from src.client.pc_client import ClientPC
from src.client.vision.shape_detection import detect_robot

# Simulated ClientPC class for testing
class SimulatedClientPC:
    def __init__(self):
        self.commands = []

    def send_command(self, command):
        print(f"Command sent: {command}")
        self.commands.append(command)

    def close_connection(self):
        print("Connection closed")

client_pc = SimulatedClientPC()

dst_size = (1200, 1800)
tolerance = 10
target_point = (900, 600)

isRobot_moving = False

# Simulated function to replace camera initialization
def initialize_simulated_camera():
    print("Simulated camera initialized")
    return "simulated_camera"

# Simulated function to replace image capture
def capture_simulated_image(camera, filename):
    print(f"Simulated image captured: {filename}")
    # Here you can copy a sample image to the target filename to simulate the capture
    sample_image = "sample_image.jpg"
    cv2.imwrite(filename, cv2.imread(sample_image))

# Initialize simulated camera
camera = initialize_simulated_camera()

# Take initial image and find corners
capture_simulated_image(camera, "test.jpg")
image = cv2.imread("test.jpg")
final_points = find_corner_points_full(image, doVerbose=True)

try:
    while True:
        # Take simulated image
        capture_simulated_image(camera, "test1.jpg")
        image = cv2.imread("test1.jpg")

        # Warp image
        gen_warped_image = warp_perspective(image, final_points, dst_size)

        # Find robot
        robot_pos, robot_direction = detect_robot(gen_warped_image)
        print(f"Robot position: {robot_pos}, direction: {robot_direction}")

        # If robot at target, stop and break
        if are_points_close(robot_pos, target_point, tolerance=100):
            client_pc.send_command("stop")
            isRobot_moving = False
            break

        # Calculate degrees to turn
        angle = rotate_vector_to_point(robot_pos, robot_direction, target_point)

        # If angle needs to change, turn robot
        if angle < -tolerance or angle > tolerance:
            if isRobot_moving:
                client_pc.send_command("stop")
                isRobot_moving = False
            client_pc.send_command(f"turn {angle}")

        # If robot not moving, start robot
        if not isRobot_moving:
            client_pc.send_command("start_drive")
            isRobot_moving = True

except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    # Cleanup resources
    client_pc.send_command("stop")
    client_pc.send_command("exit")
    client_pc.close_connection()

    print("Robot done moving")

# import cv2
#
# from src.client.field.collect_from_corner import get_ball_coordinates, robot_action_based_on_corners
# from src.client.vision.shape_detection import detect_balls
# from testing.visualization import draw_circles
#
# PIVOT_POINTS = [(300, 600), (1500, 600)]
# image_path = 'images/5.jpg'
# image = cv2.imread(image_path)
#
# if image is None:
#     print(f"Error: Unable to read image from path {image_path}")
# else:
#     print("Image successfully loaded.")
#
#     ball_coordinates, corner_results = get_ball_coordinates(image)
#     print("Detected ball coordinates:", ball_coordinates)
#
#     # Detect balls
#     circles = detect_balls(image)
#
#     # Draw detected circles
#     draw_circles(circles, image)
#
#     robot_action_based_on_corners(corner_results, client_pc,  PIVOT_POINTS)
#
#     # Save the result to a file instead of displaying it
#     output_image_path = 'images/output_detected_circles.jpg'
#     cv2.imwrite(output_image_path, image)
#     print(f"Output image saved to {output_image_path}")

import math
import numpy as np
import cv2

from src.client.field.navigate_to_target import navigate_to_target
from src.client.vision.shape_detection import detect_balls



# Mock the ClientPC class
class MockClientPC:
    def send_command(self, command):
        print(f"Mock command sent: {command}")

def mock_initialize_camera(index):
    print(f"Mock camera initialized at index {index}")
    return "mock_camera"

def mock_capture_image(camera, filename):
    print(f"Mock image captured with camera {camera} and saved as {filename}")
    # Create a mock image for testing
    mock_image = np.zeros((1200, 1800, 3), dtype=np.uint8)
    cv2.circle(mock_image, (300, 300), 50, (255, 255, 255), -1)  # Add a mock ball
    cv2.imwrite(f"images/capturedImage/{filename}", mock_image)

def mock_find_corner_points_full(image):
    print("Mock find corner points")
    return [(0, 0), (1800, 0), (0, 1200), (1800, 1200)]

def mock_warp_perspective(image, corners, dst_size):
    print("Mock warp perspective")
    return image

def mock_detect_robot(image):
    print("Mock detect robot")
    return (300, 300), 0  # Mock robot position and direction

# Use mock functions for testing
ClientPC = MockClientPC
initialize_camera = mock_initialize_camera
capture_image = mock_capture_image
find_corner_points_full = mock_find_corner_points_full
warp_perspective = mock_warp_perspective
detect_robot = mock_detect_robot

CORNERS = [(0, 0), (0, 1200), (1800, 0), (1800, 1200)]
PIVOT_POINTS = [(300, 600), (1500, 600)]
IMAGE_SIZE = [1200, 1800]

def initialize():
    global client_pc, camera
    client_pc = ClientPC()
    camera = initialize_camera(index=2)

def calculate_distance(corner_point, target_point):
    return math.sqrt((target_point[0] - corner_point[0]) ** 2 + (target_point[1] - corner_point[1]) ** 2)

def collect_from_corner(client_pc, camera, corner_point):
    capture_image(camera, "test.jpg")
    image = cv2.imread("images/capturedImage/test.jpg")
    print("Read image")
    client_pc.send_command("start_collect")

    navigate_to_target(camera, client_pc, corner_point)
    print("After navigating to the target")
    capture_image(camera, "test1.jpg")
    image = cv2.imread("images/capturedImage/test1.jpg")
    dst_size = (1200, 1800)
    gen_warped_image = warp_perspective(image, CORNERS, dst_size)
    robot_pos, robot_direction = detect_robot(gen_warped_image)
    print(f"Robot detected at {robot_pos} with direction {robot_direction}")

    client_pc.send_command("stop")

def check_corners(circles, IMAGE_SIZE, threshold=50):
    corners = {
        "top_left": (0, 0),
        "top_right": (IMAGE_SIZE[1], 0),
        "bottom_left": (0, IMAGE_SIZE[0]),
        "bottom_right": (IMAGE_SIZE[1], IMAGE_SIZE[0])
    }
    corner_results = {
        "top_left": False,
        "top_right": False,
        "bottom_left": False,
        "bottom_right": False
    }

    for x, y, radius in circles:
        if np.linalg.norm(np.array([x, y]) - np.array(corners["top_left"])) < threshold:
            print(f"Ball at ({x}, {y}) is near the top-left corner.")
            corner_results["top_left"] = True
        elif np.linalg.norm(np.array([x, y]) - np.array(corners["top_right"])) < threshold:
            print(f"Ball at ({x}, {y}) is near the top-right corner.")
            corner_results["top_right"] = True
        elif np.linalg.norm(np.array([x, y]) - np.array(corners["bottom_left"])) < threshold:
            print(f"Ball at ({x}, {y}) is near the bottom-left corner.")
            corner_results["bottom_left"] = True
        elif np.linalg.norm(np.array([x, y]) - np.array(corners["bottom_right"])) < threshold:
            print(f"Ball at ({x}, {y}) is near the bottom-right corner.")
            corner_results["bottom_right"] = True

    return corner_results

def get_ball_coordinates(camera, corner_threshold=50):
    capture_image(camera, "current_frame.jpg")
    image = cv2.imread("images/capturedImage/current_frame.jpg")

    if image is None:
        print(f"Error: Unable to read image from camera {camera}")
        return []

    image_size = image.shape
    circles = detect_balls(image)
    from testing.visualization import draw_circles
    draw_circles(circles, image)

    output_image_path = 'images/output_detected_circles.jpg'
    cv2.imwrite(output_image_path, image)
    print(f"Output image saved to {output_image_path}")

    corner_result = check_corners(circles, image_size, threshold=corner_threshold)
    return [(x, y, radius) for x, y, radius in circles], corner_result

def navigate_to_pivot(camera, client_pc, pivot_point):
    navigate_to_target(camera, client_pc, pivot_point)

def robot_action_based_on_corners(corner_results, client_pc, camera, PIVOT_POINTS):
    if corner_results["top_left"]:
        print("Ball is near the top-left corner. Robot action: move to PIVOT_POINT 0 and then collect from corner (top-left).")
        navigate_to_pivot(camera, client_pc, PIVOT_POINTS[0])
        collect_from_corner(client_pc, camera, CORNERS[0])  # top-left corner
    elif corner_results["bottom_left"]:
        print("Ball is near the bottom-left corner. Robot action: move to PIVOT_POINT 0 and then collect from corner (bottom-left).")
        navigate_to_pivot(camera, client_pc, PIVOT_POINTS[0])
        collect_from_corner(client_pc, camera, CORNERS[1])  # bottom-left corner
    elif corner_results["top_right"]:
        print("Ball is near the top-right corner. Robot action: move to PIVOT_POINT 1 and then collect from corner (top-right).")
        navigate_to_pivot(camera, client_pc, PIVOT_POINTS[1])
        collect_from_corner(client_pc, camera, CORNERS[2])  # top-right corner
    elif corner_results["bottom_right"]:
        print("Ball is near the bottom-right corner. Robot action: move to PIVOT_POINT 1 and then collect from corner (bottom-right).")
        navigate_to_pivot(camera, client_pc, PIVOT_POINTS[1])
        collect_from_corner(client_pc, camera, CORNERS[3])  # bottom-right corner
    else:
        print("No ball near any corner. Robot action: default action.")
        client_pc.send_command("default_action")


def test_collect_from_corners():
    # Initialize global variables before using them
    initialize()

    target_point = (300, 600)
    PIVOT_POINTS = [(300, 600), (1500, 600)]  # Example pivot points
    ball_coordinates, corner_results = get_ball_coordinates(camera)
    print("Detected ball coordinates:", ball_coordinates)

    # Perform robot action based on detected balls' positions relative to corners
    robot_action_based_on_corners(corner_results, client_pc, PIVOT_POINTS)

    # Cleanup resources
    # close_camera(camera)
    client_pc.send_command("exit")


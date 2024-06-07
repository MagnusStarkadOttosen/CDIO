import cv2
import numpy as np

from src.client.field.collect_from_corner import robot_action_based_on_corners, collect_from_corner
from src.client.field.coordinate_system import are_points_close, find_corner_points_full, warp_perspective
from src.client.pathfinding.CalculateCommandList import rotate_vector_to_point
from src.client.pc_client import ClientPC
from src.client.vision.camera import capture_image, initialize_camera
from src.client.vision.shape_detection import detect_robot
from src.server.ev3_server import command

print("Test collecting from corners.")
client_pc = ClientPC()

# Debugging connection status
try:
    client_pc.send_command("ping")
    print("Connected to simulator successfully.")
except Exception as e:
    print(f"Failed to connect to simulator: {str(e)}")

# Mock data for testing
circles = [(10, 10, 5), (1790, 10, 5), (10, 1190, 5), (1790, 1190, 5), (398, 765, 5)]
CORNERS = [(0, 0), (0, 1200), (1800, 0), (1800, 1200)]
PIVOT_POINTS = [(300, 600), (1500, 600)]
IMAGE_SIZE = [1200, 1800]

def navigate_to_target(client_pc, target_point, dst_size=(1200, 1800), tolerance=1):
    is_robot_moving = False

    while True:
        # Simulated robot position and direction
        robot_pos, robot_direction = (900, 600)

        # If robot at target, stop robot and break
        if are_points_close(robot_pos, target_point, tolerance=100):
            client_pc.send_command("stop")
            is_robot_moving = False
            break

        # Calculate degrees to turn
        angle = rotate_vector_to_point(robot_pos, robot_direction, target_point)
        tolerance = 10
        # Check if angle needs to change
        if angle < -tolerance or angle > tolerance:
            if is_robot_moving:
                client_pc.send_command("stop")
                is_robot_moving = False
            client_pc.send_command(f"turn {angle}")

        if not is_robot_moving:
            client_pc.send_command("start_drive")
            is_robot_moving = True
    print("Robot done moving")

def navigate_to_pivot(client_pc, pivot_point):
    navigate_to_target(client_pc, pivot_point)

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

def robot_action_based_on_corners(corner_results, client_pc, PIVOT_POINTS):
    if corner_results["top_left"]:
        print("Ball is near the top-left corner. Robot action: move to PIVOT_POINT 0 and then navigate to top-left.")
        navigate_to_pivot(client_pc, PIVOT_POINTS[0])
        client_pc.send_command(f"move_to {PIVOT_POINTS[0]}")
        navigate_to_target(client_pc, CORNERS[0])
    if corner_results["top_right"]:
        print("Ball is near the top-right corner. Robot action: move to PIVOT_POINT 1 and then navigate to top-right.")
        navigate_to_pivot(client_pc, PIVOT_POINTS[1])
        navigate_to_target(client_pc, CORNERS[1])
    if corner_results["bottom_left"]:
        print("Ball is near the bottom-left corner. Robot action: move to PIVOT_POINT 0 and then navigate to bottom-left.")
        navigate_to_pivot(client_pc, PIVOT_POINTS[0])
        navigate_to_target(client_pc, CORNERS[2])
    if corner_results["bottom_right"]:
        print("Ball is near the bottom-right corner. Robot action: move to PIVOT_POINT 1 and then navigate to bottom-right.")
        navigate_to_pivot(client_pc, PIVOT_POINTS[1])
        navigate_to_target(client_pc, CORNERS[3])
    else:
        print("No ball near any corner. Robot action: default action.")
        client_pc.send_command("default_action")

# Main script execution
try:
    corner_results = check_corners(circles, IMAGE_SIZE)
    robot_action_based_on_corners(corner_results, client_pc, PIVOT_POINTS)
    print("Delivery process started successfully.")
except Exception as e:
    print(f"An error occurred during the delivery process: {str(e)}")

# import cv2
# import numpy as np
#
# from src.client.field.collect_from_corner import robot_action_based_on_corners, collect_from_corner
# from src.client.field.coordinate_system import are_points_close, find_corner_points_full, warp_perspective
# from src.client.pathfinding.CalculateCommandList import rotate_vector_to_point
# from src.client.pc_client import ClientPC
#
# from src.client.vision.camera import capture_image, initialize_camera
# from src.client.vision.shape_detection import detect_robot
# from src.server.ev3_server import command
# from testing.test_collect_from_corners import corner_result
#
#
# print("Test collecting from corners.")
# client_pc = ClientPC()
#
# circles = [(10, 10, 5), (1790, 10, 5), (10, 1190, 5), (1790, 1190, 5), (398, 765, 5)]
# CORNERS = [(0, 0), (0, 1200), (1800, 0), (1800, 1200)]
# PIVOT_POINTS = [(300, 600), (1500, 600)]
# IMAGE_SIZE = [1200,1800]
#
# def navigate_to_target(client_pc, target_point, dst_size=(1200, 1800), tolerance=1):
#     is_robot_moving = False
#
#     while True:
#
#         # Find robot
#         robot_pos, robot_direction = (900, 600)
#
#         # If robot at target, stop robot and break
#         if are_points_close(robot_pos, target_point, tolerance=100):
#             client_pc.send_command("stop")
#             is_robot_moving = False
#             break
#
#         # Calculate degrees to turn
#         angle = rotate_vector_to_point(robot_pos, robot_direction, target_point)
#         tolerance = 10
#         # Check if angle needs to change
#         if angle < -tolerance or angle > tolerance:
#             if is_robot_moving:
#                 client_pc.send_command("stop")
#                 is_robot_moving = False
#             client_pc.send_command(f"turn {angle}")
#
#         if not is_robot_moving:
#             client_pc.send_command("start_drive")
#             is_robot_moving = True
#     print("Robot done moving")
#
# def navigat_to_pivot(client_pc, pivot_point):
#     navigate_to_target(client_pc, pivot_point)
#
# def check_corners(circles, IMAGE_SIZE, threshold=50):
#     corners = {
#         "top_left": (0, 0),
#         "top_right": (IMAGE_SIZE[1], 0),
#         "bottom_left": (0, IMAGE_SIZE[0]),
#         "bottom_right": (IMAGE_SIZE[1], IMAGE_SIZE[0])
#     }
#     corner_results = {
#         "top_left": False,
#         "top_right": False,
#         "bottom_left": False,
#         "bottom_right": False
#     }
#
#     for x, y, radius in circles:
#         if np.linalg.norm(np.array([x, y]) - np.array(corners["top_left"])) < threshold:
#             print(f"Ball at ({x}, {y}) is near the top-left corner.")
#             corner_results["top_left"] = True
#         elif np.linalg.norm(np.array([x, y]) - np.array(corners["top_right"])) < threshold:
#             print(f"Ball at ({x}, {y}) is near the top-right corner.")
#             corner_results["top_right"] = True
#         elif np.linalg.norm(np.array([x, y]) - np.array(corners["bottom_left"])) < threshold:
#             print(f"Ball at ({x}, {y}) is near the bottom-left corner.")
#             corner_results["bottom_left"] = True
#         elif np.linalg.norm(np.array([x, y]) - np.array(corners["bottom_right"])) < threshold:
#             print(f"Ball at ({x}, {y}) is near the bottom-right corner.")
#             corner_results["bottom_right"] = True
#
#     return corner_results
#
#
# def robot_action_based_on_corners(corner_results, client_pc, PIVOT_POINTS):
#     if corner_results["top_left"]:
#         print("Ball is near the top-left corner. Robot action: move to PIVOT_POINT 0 and then navigate to top-left.")
#         #client_pc.send_command(f"move_to {PIVOT_POINTS[0]} ")
#         navigat_to_pivot( client_pc, PIVOT_POINTS[0])
#         command(f"move_to {PIVOT_POINTS[0]}")
#         navigat_to_pivot( client_pc, PIVOT_POINTS[0])
#         navigate_to_target(CORNERS, client_pc, CORNERS[1])  # navigate to bottom-left
#     elif corner_results["top_right"]:
#         print("Ball is near the top-right corner. Robot action: move to PIVOT_POINT 1 and then navigate to top-right.")
#         #client_pc.send_command(f"move_to {PIVOT_POINTS[1]} ")
#         navigat_to_pivot( client_pc, PIVOT_POINTS[1])
#         navigate_to_target(CORNERS,  client_pc, CORNERS[2])  # navigate to top-right
#     elif corner_results["bottom_right"]:
#         print("Ball is near the bottom-right corner. Robot action: move to PIVOT_POINT 1 and then navigate to bottom-right.")
#         #client_pc.send_command(f"move_to {PIVOT_POINTS[1]}")
#         navigat_to_pivot(client_pc, PIVOT_POINTS[1])
#         navigate_to_target(CORNERS, client_pc, CORNERS[3])  # navigate to bottom-right
#     else:
#         print("No ball near any corner. Robot action: default action.")
#         client_pc.send_command("default_action")
#
#
#
#
# try:
#     robot_action_based_on_corners(corner_result, client_pc, PIVOT_POINTS)
#     print("Delivery process started successfully.")
# except Exception as e:
#     print(f"An error occurred during the delivery process: {str(e)}")

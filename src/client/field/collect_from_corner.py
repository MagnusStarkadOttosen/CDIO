import math
import numpy as np
from src.client.field.navigate_to_target import *
from src.client.pc_client import ClientPC


CORNERS = {
    "top_left": (0, 0),
    "bottom_left": (0, 1200),
    "top_right": (1800, 0),
    "bottom_right": (1800, 1200)
}
PIVOT_POINTS = [(300, 600), (1500, 600)]
IMAGE_SIZE = [1200, 1800]


def initialize():
    global client_pc, camera
    client_pc = ClientPC()
    camera = initialize_camera(index=2)

# def calculate_distance(corner_point, target_point):
#     return math.sqrt((target_point[0] - corner_point[0]) ** 2 + (target_point[1] - corner_point[1]) ** 2)


def ball_is_in_corner(ball_coords):
    corner_results = check_corners(ball_coords, threshold=400)
    print(f"Is ball in a corner? {any(corner_results.values())}")
    return any(corner_results.values())



def check_corners(ball_coords, threshold=100):

        corner_result = {
            "top_left": False,
            "top_right": False,
            "bottom_left": False,
            "bottom_right": False
        }

        x, y = ball_coords
        for corner_name, corner_coords in CORNERS.items():
            if np.linalg.norm(np.array([x, y]) - np.array(corner_coords)) < threshold:
                print(f"Ball at ({x}, {y}) is near the {corner_name} corner.")
                corner_result[corner_name] = True

        return corner_result


def get_corner_with_displacement(corner_results, current_position):
    if corner_results["top_left"]:
        displacement = calculate_displacement(CORNERS["top_left"], current_position)
        print("Ball is near the top-left corner. Robot action: move directly to top-left.")
        return CORNERS["top_left"], displacement
    elif corner_results["bottom_left"]:
        displacement = calculate_displacement(CORNERS["bottom_left"], current_position)
        print("Ball is near the bottom-left corner. Robot action: move directly to bottom-left.")
        return CORNERS["bottom_left"], displacement
    elif corner_results["top_right"]:
        displacement = calculate_displacement(CORNERS["top_right"], current_position)
        print("Ball is near the top-right corner. Robot action: move directly to top-right.")
        return CORNERS["top_right"], displacement
    elif corner_results["bottom_right"]:
        displacement = calculate_displacement(CORNERS["bottom_right"], current_position)
        print("Ball is near the bottom-right corner. Robot action: move directly to bottom-right.")
        return CORNERS["bottom_right"], displacement
    else:
        print("No ball near any corner")
        return False, (0, 0)
# def robot_movement_based_on_corners(corner_results, robot_pos):
#     if corner_results["top_left"]:
#         target_corner = CORNERS["top_left"]
#         print("Ball is near the top-left corner. Robot action: move directly to top-left.")
#     elif corner_results["bottom_left"]:
#         target_corner = CORNERS["bottom_left"]
#         print("Ball is near the bottom-left corner. Robot action: move directly to bottom-left.")
#     elif corner_results["top_right"]:
#         target_corner = CORNERS["top_right"]
#         print("Ball is near the top-right corner. Robot action: move directly to top-right.")
#     elif corner_results["bottom_right"]:
#         target_corner = CORNERS["bottom_right"]
#         print("Ball is near the bottom-right corner. Robot action: move directly to bottom-right.")
#     else:
#         print("No ball near any corner")
#         return None, None
#
#     displacement = calculate_displacement(robot_pos, target_corner)
#     angle = calculate_angle(robot_pos, target_corner)
#     return target_corner, displacement, angle

def calculate_displacement(robot_pos, target_pos):
    displacement_vector = (target_pos[0] - robot_pos[0], target_pos[1] - robot_pos[1])
    print(f"Calculated displacement vector: {displacement_vector}")
    return displacement_vector

# def calculate_angle(direction, target_vector):
#     norm_dir = np.linalg.norm(direction)
#     norm_tar = np.linalg.norm(target_vector)
#     if norm_dir == 0 or norm_tar == 0:
#         return 0
#     cos_theta = np.dot(direction, target_vector) / (norm_dir * norm_tar)
#     angle = np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))
#     return angle if np.cross(direction, target_vector) >= 0 else -angle

# def calculate_angle(robot_pos, target_pos):
#     delta_x = target_pos[0] - robot_pos[0]
#     delta_y = target_pos[1] - robot_pos[1]
#     angle = math.degrees(math.atan2(delta_y, delta_x))
#     print(f"Calculated angle: {angle} degrees")
#     return angle
# def robot_movement_based_on_corners(corner_results):
#     if corner_results["top_left"]:
#         print("Ball is near the top-left corner. Robot action: move to PIVOT_POINT 0 and then navigate to top-left.")
#         return PIVOT_POINTS[0],CORNERS[0]
#     elif corner_results["bottom_left"]:
#         print("Ball is near the bottom-left corner. Robot action: move to PIVOT_POINT 0 and then navigate to bottom-left.")
#         return PIVOT_POINTS[0], CORNERS[1]
#     elif corner_results["top_right"]:
#         print("Ball is near the top-right corner. Robot action: move to PIVOT_POINT 1 and then navigate to top-right.")
#         print(f"pivot: {PIVOT_POINTS[1]} corner: {(1800, 0)}")
#
#         return PIVOT_POINTS[1], (1800, 0)
#     elif corner_results["bottom_right"]:
#         print("Ball is near the bottom-right corner. Robot action: move to PIVOT_POINT 1 and then navigate to bottom-right.")
#         return PIVOT_POINTS[1], CORNERS["bottom_right"]
#     else:
#         print("No ball near any corner")
#         return False

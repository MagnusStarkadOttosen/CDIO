
import math

import numpy as np

from src.client.field.navigate_to_target import *
from src.client.pc_client import ClientPC

CORNERS = [(0, 0), (0, 1200), (1800, 0), (1800, 1200)]
PIVOT_POINTS = [(300, 600), (1500, 600)]
IMAGE_SIZE = [1200,1800]


def initialize():
    global client_pc, camera
    client_pc = ClientPC()
    camera = initialize_camera(index=2)

def calculate_distance(corner_point, target_point):
    return math.sqrt((target_point[0] - corner_point[0]) ** 2 + (target_point[1] - corner_point[1]) ** 2)


def is_ball_in_corner(ball_coords):
 return is_ball_in_corner(ball_coords)


def check_corners(ball_coords, threshold=50):

        corner_result = {
            (0, 0): False,  # top_left
            (IMAGE_SIZE[1], 0): False,  # top_right
            (0, IMAGE_SIZE[0]): False,  # bottom_left
            (IMAGE_SIZE[1], IMAGE_SIZE[0]): False  # bottom_right
        }

        x, y, radius = ball_coords
        for corner_coords in corner_result:
            if np.linalg.norm(np.array([x, y]) - np.array(corner_coords)) < threshold:
                print(f"Ball at ({x}, {y}) is near the corner at {corner_coords}.")
                corner_result[corner_coords] = True

        return corner_result


def robot_movement_based_on_corners(corner_results):
    if corner_results["top_left"]:
        print("Ball is near the top-left corner. Robot action: move to PIVOT_POINT 0 and then navigate to top-left.")
        return PIVOT_POINTS[0],CORNERS[0]
    elif corner_results["bottom_left"]:
        print("Ball is near the bottom-left corner. Robot action: move to PIVOT_POINT 0 and then navigate to bottom-left.")
        return PIVOT_POINTS[0], CORNERS[1]
    elif corner_results["top_right"]:
        print("Ball is near the top-right corner. Robot action: move to PIVOT_POINT 1 and then navigate to top-right.")
        return PIVOT_POINTS[1], CORNERS[2]
    elif corner_results["bottom_right"]:
        print("Ball is near the bottom-right corner. Robot action: move to PIVOT_POINT 1 and then navigate to bottom-right.")
        return PIVOT_POINTS[1], CORNERS[3]
    else:
        print("No ball near any corner")

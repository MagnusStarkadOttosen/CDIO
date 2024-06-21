
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

def calculate_distance(corner_point, target_point):
    return math.sqrt((target_point[0] - corner_point[0]) ** 2 + (target_point[1] - corner_point[1]) ** 2)


def is_ball_in_corner(ball_coords):
    corner_results = check_corners(ball_coords, threshold=400)
    print(f"Is ball in a corner? {any(corner_results.values())}")
    return any(corner_results.values())



def check_corners(ball_coords, threshold=50):

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


def get_pivot_and_corner(corner_results):
    if corner_results["top_left"]:
        print("Ball is near the top-left corner. Robot action: move to PIVOT_POINT 0 and then navigate to top-left.")
        return PIVOT_POINTS[0],CORNERS["top_left"]
    elif corner_results["bottom_left"]:
        print("Ball is near the bottom-left corner. Robot action: move to PIVOT_POINT 0 and then navigate to bottom-left.")
        return PIVOT_POINTS[0], CORNERS["bottom_left"]
    elif corner_results["top_right"]:
        print("Ball is near the top-right corner. Robot action: move to PIVOT_POINT 1 and then navigate to top-right.")
        return PIVOT_POINTS[1], CORNERS["top_right"]
    elif corner_results["bottom_right"]:
        print("Ball is near the bottom-right corner. Robot action: move to PIVOT_POINT 1 and then navigate to bottom-right.")
        return PIVOT_POINTS[1], CORNERS["bottom_right"]
    else:
        print("No ball near any corner")
        return False

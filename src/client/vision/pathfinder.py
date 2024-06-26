import numpy as np

from src.client.utilities import get_distance


def balls_are_remaining(circles):
    if circles is not None:
        return True
    else:
        return False


def find_nearest_ball(robot_pos, circles):
    ball_pos = np.array([0, 0])
    nearest = 300000
    for (x, y, r) in circles:
        dist = get_distance(robot_pos, np.array([x, y]))
        if dist < nearest:
            ball_pos[0] = x
            ball_pos[1] = y
            nearest = dist
    return ball_pos
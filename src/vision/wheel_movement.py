import math
import numpy as np

from src.vision.shape_detection import Pos

WHEEL_DIMENSION = 80
WHEEL_CIRCUMF_CM = WHEEL_DIMENSION * math.pi


#def get_degrees_to_pivot(current_robot_orientation):
    #current_robot_orientation

def get_wheel_rotation(distance_to_move):
    rotations = distance_to_move / WHEEL_CIRCUMF_CM
    degrees_to_move = rotations * 360
    return degrees_to_move


def get_distance_to_move(robot_pos: Pos, target_pos: Pos):
    dist_x = robot_pos.x - target_pos.x
    dist_y = robot_pos.y - target_pos.y
    distance = np.round(math.sqrt(dist_x ** 2 + dist_y ** 2), 1)
    print(distance)
    return distance


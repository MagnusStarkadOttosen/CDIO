import math

from src.vision.shape_detection import Pos

WHEEL_DIMENSION = 80
WHEEL_CIRCUMF_CM = WHEEL_DIMENSION * math.pi


#def get_degrees_to_pivot(current_robot_orientation):
    #current_robot_orientation

def get_wheel_revolutions(distance_to_move):
    revolutions = distance_to_move / WHEEL_CIRCUMF_CM
    revolution_degrees = revolutions * 360
    return revolution_degrees


def get_distance_to_move(robot_pos: Pos, target_pos: Pos):
    dist_x = robot_pos.x - target_pos.x
    dist_y = robot_pos.y - target_pos.y
    distance = round(math.sqrt(dist_x ** 2 + dist_y ** 2), 1)
    return distance


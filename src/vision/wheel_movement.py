import math

from src.vision.shape_detection import Pos


WHEEL_DIMENSION = 55
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
    distance = round(math.sqrt(dist_x ** 2 + dist_y ** 2), 1)
    return distance

def move_robot_distance(distance_to_move_cm):
    degrees_to_move = get_wheel_rotation(distance_to_move_cm)
    return degrees_to_move


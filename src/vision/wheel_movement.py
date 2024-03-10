import math


def get_distance_to_move(robot_pos, target_pos):
    dist_vector = robot_pos - target_pos
    distance = round(math.sqrt(dist_vector[0] ** 2 + dist_vector[1] ** 2), 1)
    return distance


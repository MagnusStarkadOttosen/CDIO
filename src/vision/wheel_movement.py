import math


def get_distance_to_move(robot_pos, target_pos):
    dist_vector = robot_pos - target_pos
    print('Calculate dist vector: ', dist_vector)
    distance = round(math.sqrt(dist_vector[0] ** 2 + dist_vector[1] ** 2), 1)
    """dist_x = robot_pos.x - target_pos.x
    dist_y = robot_pos.y - target_pos.y
    distance = round(math.sqrt(dist_x ** 2 + dist_y ** 2), 1)"""
    return distance


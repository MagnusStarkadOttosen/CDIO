import math


def get_distance_to_move(robot_pos, target_pos):
    dist_vector = robot_pos - target_pos
    distance = round(math.sqrt(dist_vector[0] ** 2 + dist_vector[1] ** 2), 1)
    return distance

def get_degrees_to_pivot(robot_pos: Pos, target_pos: Pos):
    
    dist_x = robot_pos.x - target_pos.x
    dist_y = robot_pos.y - target_pos.y
    angle = math.degrees(math.atan2(dist_y, dist_x))
    return angle



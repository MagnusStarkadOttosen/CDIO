import math

from src.server.robot import Pos


#def get_degrees_to_pivot(current_robot_orientation):
    #current_robot_orientation


def get_distance_to_move(robot_pos: Pos, target_pos: Pos):
    dist_x = robot_pos.x - target_pos.x
    dist_y = robot_pos.y - target_pos.y
    distance = round(math.sqrt(dist_x ** 2 + dist_y ** 2), 1)
    return distance


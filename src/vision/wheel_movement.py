#!/usr/bin/env python3

import math

WHEEL_DIMENSION = 80
WHEEL_CIRCUMF_CM = WHEEL_DIMENSION * math.pi


class Pos:
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y


# def move_robot

def get_wheel_rotation(distance_to_move):
    rotations = distance_to_move / WHEEL_CIRCUMF_CM
    degrees_to_move = rotations * 360
    return degrees_to_move


def get_distance_to_move(robot_pos: Pos, target_pos: Pos):
    dist_x = abs(robot_pos.x - target_pos.x)
    dist_y = abs(robot_pos.y - target_pos.y)
    distance = round(math.sqrt(dist_x ** 2 + dist_y ** 2), 1)
    return distance


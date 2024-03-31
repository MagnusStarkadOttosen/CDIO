import math
import numpy as np

WHEEL_DIMENSION = 80
WHEEL_CIRCUMF_CM = WHEEL_DIMENSION * math.pi
ROBOT_START_X = 10
ROBOT_START_Y = 20


"""
class Robot:

    def __init__(self):
        self.position = np.array([ROBOT_START_X, ROBOT_START_Y], dtype=int)
        self.pivot = 0

    def get_position(self):
        return self.position
"""

def drive(distance_to_move):
    revs = get_wheel_revolutions(distance_to_move)
    print('Wheel motor turning this many degrees: ', revs)  # Placeholder


def turn(degrees_to_rotate):
    print('Turning this many degrees: ', degrees_to_rotate)  # Placeholder


def get_wheel_revolutions(distance_to_move):
    revolutions = distance_to_move / WHEEL_CIRCUMF_CM
    revolution_degrees = revolutions * 360
    return revolution_degrees


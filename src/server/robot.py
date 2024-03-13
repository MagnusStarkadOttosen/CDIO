import math
import numpy as np
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D, SpeedPercent
from ev3dev2._platform.ev3 import INPUT_2


WHEEL_DIMENSION = 80
WHEEL_CIRCUMF_CM = WHEEL_DIMENSION * math.pi
ROBOT_START_X = 10
ROBOT_START_Y = 20


class Robot:
    tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
    def __init__(self):
        self.position = np.array([ROBOT_START_X, ROBOT_START_Y], dtype=int)
        self.pivot = 0

    def get_position(self):
        return self.position


def move(distance_to_move, tank_drive):
    revs = get_wheel_revolutions(distance_to_move)
    print('Wheel motor turning this many degrees: ', revs)  # Placeholder
    tank_drive.on_for_degrees(SpeedPercent(30), SpeedPercent(30), revs)
    tank_drive.stop()


def turn(degrees_to_rotate):
    print('Turning this many degrees: ', degrees_to_rotate)  # Placeholder


def get_wheel_revolutions(distance_to_move):
    revolutions = distance_to_move / WHEEL_CIRCUMF_CM
    revolution_degrees = revolutions * 360
    return revolution_degrees


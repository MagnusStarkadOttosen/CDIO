import math

WHEEL_DIMENSION = 80
WHEEL_CIRCUMF_CM = WHEEL_DIMENSION * math.pi
ROBOT_START_X = 10
ROBOT_START_Y = 20


class Pos:
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y


class Robot:

    def __init__(self):
        self.position = Pos(ROBOT_START_X, ROBOT_START_Y)
        self.pivot = 0


def drive(distance_to_move):
    revs = get_wheel_revolutions(distance_to_move)
    print('Wheel motor turning this many degrees: ', revs)  # Placeholder


def turn(degrees_to_rotate):
    print('Turning this many degrees: ', degrees_to_rotate)  # Placeholder


def get_wheel_revolutions(distance_to_move):
    revolutions = distance_to_move / WHEEL_CIRCUMF_CM
    revolution_degrees = revolutions * 360
    return revolution_degrees

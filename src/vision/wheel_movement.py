import math

WHEEL_DIMENSION = 80
DISTANCE_TO_MOVE = 70  # For test
WHEEL_CIRCUMF_CM = WHEEL_DIMENSION * math.pi


class Pos:
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y


def wheel_rotation():
    wheel_circumferenc_cm = math.pi * WHEEL_DIMENSION
    rotations = DISTANCE_TO_MOVE / wheel_circumferenc_cm
    degrees_to_move = rotations * 360
    return degrees_to_move


def get_distance_to_move(robot_pos: Pos, target_pos: Pos):
    return math.sqrt(
        abs(robot_pos.x - target_pos.x) ** 2 +
        abs(robot_pos.y - target_pos.y) ** 2
    )


def get_wheel_rotation(distance_to_move):
    rotations = distance_to_move / WHEEL_CIRCUMF_CM
    degrees_to_move = rotations * 360
    return degrees_to_move

import math

import src.client.field.field_objects.robot
import src.client.utilities

WHEEL_DIMENSION = 80
WHEEL_CIRCUMF_CM = WHEEL_DIMENSION * math.pi


# calculate the distance the robot needs to move to reach the target position
# def get_distance_to_move(self, target_pos):
#         b = math.sqrt((target_pos[0] - self.M[0]) ** 2 + (target_pos[1] - self.M[1]) ** 2)
#         return b

# calculate the degrees between the vector MB and the vector MC
# determine the robot's rotation direction relative to the target position ( turn left or turn right)
# the robot's position is updated after the robot turns

def generate_turn_command(self, target_pos):
    degrees = src.client.field.field_objects.robot.get_degrees_to_rotation(target_pos)
    if degrees > 0:
        command = f"rotate {abs(degrees)}"
    elif degrees < 0:
        command = f"rotate {abs(degrees)}"
    else:
        command = f"move {src.client.utilities.get_distance(target_pos, )}"

    return command


class Pos:
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y

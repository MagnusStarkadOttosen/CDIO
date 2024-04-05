import math

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
def get_degrees_to_rotation(self, target_pos):
         # distance MB = a
        a = math.sqrt((self.B[0] - self.M[0]) ** 2 + (self.B[1] - self.M[1]) ** 2)
        # distance MC = b
        b = math.sqrt((target_pos[0] - self.M[0]) ** 2 + (target_pos[1] - self.M[1]) ** 2)
        # distance BC = c
        c = math.sqrt((target_pos[0] - self.B[0]) ** 2 + (target_pos[1] - self.B[1]) ** 2)
        #radian of angle between vector MB and vector MC
        radian = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
        #degrees of angle between vector MB and vector MC
        degrees = math.degrees(radian)
        # determine the robot's rotation direction relative to the target position
        # turn left or turn right
        # Calculate direction vectors
        MB = (self.B[0] - self.M[0], self.B[1] - self.M[1])
        MTarget = (target_pos[0] - self.M[0], target_pos[1] - self.M[1])

     # Calculate the cross product's Z component
        cross_product_z = MB[0] * MTarget[1] - MB[1] * MTarget[0]

    # Determine direction based on the cross product's sign
        if cross_product_z > 0:
            return -degrees
        elif cross_product_z < 0:
            return degrees
        else: 
            return 0

def generate_turn_command(self, target_pos):
    degrees = self.get_degrees_to_rotation(target_pos)
    if degrees > 0:
        command = f"rotate {abs(degrees)}"
    elif degrees < 0:
        command = f"rotate {abs(degrees)}"
    else:
        command = f"move {src.client.utilities.get_distance(target_pos)}"

    return command


class Pos:
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y

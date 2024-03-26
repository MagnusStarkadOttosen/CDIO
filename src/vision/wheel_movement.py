import math

from src.vision.shape_detection import Pos

WHEEL_DIMENSION = 80
WHEEL_CIRCUMF_CM = WHEEL_DIMENSION * math.pi


#def get_degrees_to_pivot(current_robot_orientation):
    #current_robot_orientation

def get_wheel_rotation(distance_to_move):
    rotations = distance_to_move / WHEEL_CIRCUMF_CM
    degrees_to_move = rotations * 360
    return degrees_to_move


def get_distance_to_move(robot_pos: Pos, target_pos: Pos):
    dist_x = robot_pos.x - target_pos.x
    dist_y = robot_pos.y - target_pos.y
    distance = round(math.sqrt(dist_x ** 2 + dist_y ** 2), 1)
    return distance

def get_degrees_to_pivot(robot_pos: Pos, target_pos: Pos):
    
    dist_x = robot_pos.x - target_pos.x
    dist_y = robot_pos.y - target_pos.y
    angle = math.degrees(math.atan2(dist_y, dist_x))
    return angle


def get_distance_to_move(self, target_pos):
        b = math.sqrt((target_pos[0] - self.M[0]) ** 2 + (target_pos[1] - self.M[1]) ** 2)
        return b


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
            return degrees
        elif cross_product_z < 0:
            return -degrees
        else: 
            return 0


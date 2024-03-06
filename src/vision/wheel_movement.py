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

# def get_degrees_to_turn() is determined based on the position of the target (ball) in relation to the robot's quadrant,
# and the angle of the line between the robot and the target when robot's direction is 0 degrees.
def get_degrees_to_turn(target_pos:Pos):
    tan_target = target_pos.y / target_pos.x
    angle_radians = math.atan(tan_target)
    target_degrees = math.degrees(angle_radians)
    if target_pos.x >0 and target_pos.y>0:
        degrees_to_turn = target_degrees
        return degrees_to_turn
    elif target_pos.x<0 and target_pos.y>0:
        degrees_to_turn = 180 -target_degrees
        return degrees_to_turn
    elif target_pos.x<0 and target_pos.y<0:
        degrees_to_turn = -(180 - target_degrees)
        return degrees_to_turn
    elif target_pos.x>0 and target_pos.y<0:
        degrees_to_turn = target_degrees-90
        return degrees_to_turn





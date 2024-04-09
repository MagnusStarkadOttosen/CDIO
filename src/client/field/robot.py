import math

WHEEL_DIMENSION = 5.5
DIST_BETWEEN_WHEELS = 13.5
WHEEL_CIRCUMF_CM = WHEEL_DIMENSION * math.pi


def calc_vector_direction(end_point, start_point):
    direction = (end_point[0] - start_point[0], end_point[1] - start_point[1])
    return direction


def angle_between_vectors(vector_a, vector_b):
    dot_product_ab = _dot_product(vector_a, vector_b)
    length_a = _vector_length(vector_a)
    length_b = _vector_length(vector_b)
    cos_theta = dot_product_ab / (length_a * length_b)
    theta_radians = math.acos(cos_theta)
    return math.degrees(theta_radians)


def _dot_product(vector_a, vector_b):
    return sum(a * b for a, b in zip(vector_a, vector_b))


def _vector_length(vector):
    return math.sqrt(sum(x ** 2 for x in vector))


def calc_degrees_to_rotate(robot_direction, target_direction):
    degrees = angle_between_vectors(robot_direction, target_direction)

    # Calculate the cross product's Z component
    cross_product_z = (robot_direction[0] * target_direction[1]
                       - robot_direction[1] * target_direction[0])

    # Determine direction based on the cross product's sign
    if cross_product_z > 0:
        return -degrees
    elif cross_product_z < 0:
        return degrees
    else:
        return 0


# modified robot class with position and pivot
# the robot's position in the coordinate system with two points ( red and green) is called A and B
# A and B is get from the image detection with the red and green points from decetor_robot.py
# M is the intersection point between the line AB and the wheel axis with distan M to A is 10 cm
# M is the robot's position

# the robot's position is updated after the robot moves or turns
# the pivot is updated after the robot turns
# the robot's position is updated after the robot moves

# class Robot:
#     def __init__(self):
#         self.red_dot = None  # red point's coordinates
#         self.green_dot = None  # green point's coordinates
#         self.pos = None  # the robot's position
#         self.pivot = 0  # the angle between the vector pos->green and vector pos->ball_pos


# def update_pivot_from_image(robot_pos, ball_pos):
#     # self.C = target_pos # There is no member C in Robot??
#     return get_degrees_to_rotate(robot_pos, ball_pos)
#
#
# def move(self, target_pos):
#     # distance to move is the distance from M to the target position
#     # the robot's position is updated after the robot moves
#     get_distance(self, target_pos)
#     self.pos = target_pos
#     return self.pos

# def calc_degrees_to_rotate(robot_pos, green_dot, target_pos, robot_direction):
#     # distance robot_pos -> green_dot = a
#     # a = math.sqrt(robot_direction[0] ** 2 + robot_direction[1] ** 2)
#
#     # distance robot_pos -> target_pos = b
#     # b = math.sqrt((target_pos[0] - robot_pos[0]) ** 2 + (target_pos[1] - robot_pos[1]) ** 2)
#
#     # distance green_dot -> target_pos = c
#     # c = math.sqrt((target_pos[0] - green_dot[0]) ** 2 + (target_pos[1] - green_dot[1]) ** 2)
#
#     # vector between robot_pos -> green_dot and robot_pos->target_pos
#     # vect_ab = _tuple_subtract(b, a)
#     # c = vect_ab
#     # radian of angle between vector pos_to_green_dot and vector robot_pos->target_pos
#     # radian = math.acos((a ** 2 + b ** 2 - c ** 2)
#     #                   / (2 * a * b))
#
#
#     # degrees of angle between vector pos_to_green_dot and vector robot_pos->target_pos
#     # degrees = math.degrees(radian)
#
#     # determine the robot's rotation direction relative to the target position
#     # turn left or turn right
#     # Calculate direction vectors
#     pos_to_green_dot = (green_dot[0] - robot_pos[0], green_dot[1] - robot_pos[1])
#     pos_to_target = (target_pos[0] - robot_pos[0], target_pos[1] - robot_pos[1])
#
#     # Calculate the cross product's Z component
#     cross_product_z = pos_to_green_dot[0] * pos_to_target[1] - pos_to_green_dot[1] * pos_to_target[0]
#
#     # Determine direction based on the cross product's sign
#     if cross_product_z > 0:
#         return -degrees
#     elif cross_product_z < 0:
#         return degrees
#     else:
#         return 0


# def calc_robot_pos(green_dot, red_dot):
#     distance = math.sqrt(
#         (green_dot[0] - red_dot[0]) ** 2 + (green_dot[1] - red_dot[1]) ** 2)
#
#     # distance from red_dot to robot_pos :a
#     a = 45
#
#     pos = (red_dot[0] + a / (distance * (green_dot[0] - red_dot[0])),
#            red_dot[1] + a / (distance * (green_dot[1] - red_dot[1])))
#
#     print(f"robot_pos: {pos}")
#     return pos

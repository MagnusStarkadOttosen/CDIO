import math

def rotate_vector_to_point(robot_pos, robot_direction, target_pos):
    """
    Calculate the angle by which the robot needs to rotate to accurately face the target position.

    :param robot_pos: Tuple (x, y) representing the robot's current position.
    :param robot_direction: Tuple (dx, dy) representing the robot's current facing direction.
    :param target_pos: Tuple (x, y) representing the target's position.
    :return: Float representing the angle in degrees that the robot needs to rotate.
             Positive values mean clockwise rotation, negative values mean counterclockwise rotation.
    """
    # Calculate the direction vector from the robot to the target
    target_vector = (target_pos[0] - robot_pos[0], target_pos[1] - robot_pos[1])

    # Normalize the direction vectors
    robot_magnitude = math.sqrt(robot_direction[0]**2 + robot_direction[1]**2)
    target_magnitude = math.sqrt(target_vector[0]**2 + target_vector[1]**2)
    normalized_robot_direction = (robot_direction[0] / robot_magnitude, robot_direction[1] / robot_magnitude)
    normalized_target_vector = (target_vector[0] / target_magnitude, target_vector[1] / target_magnitude)

    # Compute the dot product and the determinant for angle and direction
    dot_product = normalized_robot_direction[0] * normalized_target_vector[0] + normalized_robot_direction[1] * normalized_target_vector[1]
    determinant = normalized_robot_direction[0] * normalized_target_vector[1] - normalized_robot_direction[1] * normalized_target_vector[0]

    # Calculate the angle in radians and convert to degrees
    angle = math.acos(dot_product)  # acos returns value between 0 and π
    angle_degrees = math.degrees(angle)

    # Determine the direction of the rotation based on the determinant
    if determinant > 0:
        return angle_degrees  # Positive for counterclockwise rotation
    else:
        return -angle_degrees  # Negative for clockwise rotation

# Example usage:
robot_pos = (158, 983)
robot_direction = (0, -161)  # Assuming this is normalized direction
target_point = (900, 600)
angle = rotate_vector_to_point(robot_pos, robot_direction, target_point)
print(f"Rotate by {angle:.2f} degrees")

# import math
#
# def rotate_vector_to_point(robot_pos, robot_direction, target):
#     #Calculate the direction to target
#     direction = (target[0] - robot_pos[0], target[1] - robot_pos[1])
#
#     #Calculate the dot product
#     dot_product = robot_direction[0] * direction[0] + robot_direction[1] * direction[1]
#
#     #Calculate magnitudes of the vectors
#     vector_mag = math.sqrt(robot_direction[0]**2 + robot_direction[1]**2)
#     direction_mag = math.sqrt(direction[0]**2 + direction[1]**2)
#
#     #Calculate cosine of the angle using the dot product formula
#     cos_theta = dot_product / (vector_mag * direction_mag)
#
#     #Handle floating point precision issues
#     #acos need a value between -1 and 1. Values like 1.000000001 is posible and need to be removed
#     cos_theta = max(-1, min(1, cos_theta))
#
#     #Calculate the angle in degrees
#     angle = math.acos(cos_theta)
#     angle_degrees = angle * (180 / math.pi)
#
#     #Calculate the determinant to find the rotation direction
#     determinant = robot_direction[0] * direction[1] - robot_direction[1] * direction[0]
#     if(determinant < 0): #CounterClockwise
#         angle_degrees *= -1
#
#     return angle_degrees
# #test
# robot_pos = (158, 983)
# robot_direction = (0, -161)
# target_point = (900, 600)
# angle = rotate_vector_to_point(robot_pos, robot_direction, target_point)
# print(f"Rotate by {angle:.2f} degrees")
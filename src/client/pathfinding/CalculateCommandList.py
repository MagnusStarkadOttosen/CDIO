import math

def rotate_vector_to_point(robot_pos, robot_direction, target):
    #Calculate the direction to target
    direction = (target[0] - robot_pos[0], target[1] - robot_pos[1])

    #Calculate the dot product
    dot_product = robot_direction[0] * direction[0] + robot_direction[1] * direction[1]

    #Calculate magnitudes of the vectors
    vector_mag = math.sqrt(robot_direction[0]**2 + robot_direction[1]**2)
    direction_mag = math.sqrt(direction[0]**2 + direction[1]**2)

    #Calculate cosine of the angle using the dot product formula
    cos_theta = dot_product / (vector_mag * direction_mag)

    #Handle floating point precision issues
    #acos need a value between -1 and 1. Values like 1.000000001 is posible and need to be removed
    cos_theta = max(-1, min(1, cos_theta))

    #Calculate the angle in degrees
    angle = math.acos(cos_theta)
    angle_degrees = angle * (180 / math.pi)

    #Calculate the determinant to find the rotation direction
    determinant = robot_direction[0] * direction[1] - robot_direction[1] * direction[0]
    if(determinant < 0): #CounterClockwise
        angle_degrees *= -1

    return angle_degrees

#test
robot_pos = (158, 983)
robot_direction = (0, -161)
target_point = (900, 600)
angle = rotate_vector_to_point(robot_pos, robot_direction, target_point)
print(f"Rotate by {angle:.2f} degrees")
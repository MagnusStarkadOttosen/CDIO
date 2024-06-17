import math

def rotate_vector_to_point(robot_pos, robot_direction, target):
    # Calculate the direction to target
    direction = (target[0] - robot_pos[0], target[1] - robot_pos[1])
    print(f"Direction to target: {direction}")

    # Normalize robot_direction
    vector_mag = math.sqrt(robot_direction[0]**2 + robot_direction[1]**2)
    if vector_mag != 0:
        robot_direction = (robot_direction[0] / vector_mag, robot_direction[1] / vector_mag)
    print(f"Normalized robot direction: {robot_direction}")

    # Calculate the dot product
    dot_product = robot_direction[0] * direction[0] + robot_direction[1] * direction[1]
    print(f"Dot Product: {dot_product}")

    # Calculate magnitudes of the direction vector
    direction_mag = math.sqrt(direction[0]**2 + direction[1]**2)
    print(f"Direction Magnitude: {direction_mag}")

    # Normalize direction vector
    if direction_mag != 0:
        direction = (direction[0] / direction_mag, direction[1] / direction_mag)
    print(f"Normalized direction to target: {direction}")

    # Calculate cosine of the angle using the dot product formula
    cos_theta = dot_product / (1 * direction_mag)  # robot_direction is now a unit vector
    print(f"Cosine Theta: {cos_theta}")

    # Handle floating point precision issues
    cos_theta = max(-1, min(1, cos_theta))

    # Calculate the angle in degrees
    angle = math.acos(cos_theta)
    angle_degrees = angle * (180 / math.pi)
    print(f"Angle (degrees): {angle_degrees}")

    # Calculate the determinant to find the rotation direction
    determinant = robot_direction[0] * direction[1] - robot_direction[1] * direction[0]
    print(f"Determinant: {determinant}")
    if determinant < 0:  # CounterClockwise
        angle_degrees *= -1

    print(f"Calculated turn angle: {angle_degrees}")
    return angle_degrees

#test
robot_pos = (158, 983)
robot_direction = (0, -161)
target_point = (900, 600)
angle = rotate_vector_to_point(robot_pos, robot_direction, target_point)
print(f"Rotate by {angle:.2f} degrees")
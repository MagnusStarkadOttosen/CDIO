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

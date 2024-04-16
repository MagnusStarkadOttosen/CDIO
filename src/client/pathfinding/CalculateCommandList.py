import math

def rotate_vector_to_point(red_point, green_point, target):
    #Convert input tuples to vectors
    vector = (green_point[0] - red_point[0], green_point[1] - red_point[1])
    direction = (target[0] - red_point[0], target[1] - red_point[1])

    #Calculate the dot product
    dot_product = vector[0] * direction[0] + vector[1] * direction[1]

    #Calculate magnitudes of the vectors
    vector_mag = math.sqrt(vector[0]**2 + vector[1]**2)
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
    determinant = vector[0] * direction[1] - vector[1] * direction[0]
    if(determinant > 0): #CounterClockwise
        angle_degrees *= -1

    return angle_degrees

#test
red = (1, 1)
green = (2, 1)
target_point = (3, 3)
angle = rotate_vector_to_point(red, green, target_point)
print(f"Rotate by {angle:.2f} degrees")
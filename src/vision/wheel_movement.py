import math

WHEEL_DIMENSION = 80
DISTANCE_TO_MOVE = 70 # For test

def wheel_rotation():
    wheel_circumferenc_cm = math.pi * WHEEL_DIMENSION
    rotations = DISTANCE_TO_MOVE / wheel_circumferenc_cm
    degrees_to_move  = rotations * 360
    return  degrees_to_move


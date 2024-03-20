import math
import time

from ev3dev2.motor import (MoveTank, OUTPUT_A, OUTPUT_D, SpeedPercent)
from ev3dev2.sensor.lego import GyroSensor

WHEEL_DIMENSION = 5.5
WHEEL_CIRCUMF_CM = WHEEL_DIMENSION * math.pi
ROBOT_START_X = 10
ROBOT_START_Y = 20
tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
# Initialize the tank's gyro sensor
tank_drive.gyro = GyroSensor()
tank_drive.gyro.mode = 'GYRO-ANG'
time.sleep(1)

# Calibrate the gyro to eliminate drift, and to initialize the current angle as 0
tank_drive.gyro.reset()

# Pivot 30 degrees

"""
class Robot:

    def __init__(self):
        self.position = np.array([ROBOT_START_X, ROBOT_START_Y], dtype=int)
        self.pivot = 0

    def get_position(self):
        return self.position
"""


# Function to turn the robot by x degrees
def turn_by_x_degrees(x):
    # Record the starting angle
    start_angle = tank_drive.gyro.angle
    speed = 25
    # Determine the direction of rotation
    if x > 0:
        # Positive x, turn right
        tank_drive.on(left_speed=speed, right_speed=-speed)
    else:
        # Negative x, turn left
        tank_drive.on(left_speed=-speed, right_speed=speed)

    # Wait until the robot has turned x degrees
    while abs(tank_drive.gyro.angle - start_angle) < abs(x):
        time.sleep(0.1)

    # Stop the motors once the turn is complete
    tank_drive.off()

def drive(distance_to_move):
    # revs = get_wheel_revolutions(distance_to_move)
    degrees = convert_distance_to_degrees(distance_to_move)
    tank_drive.on_for_degrees(SpeedPercent(30), SpeedPercent(30), degrees)
    print('Wheel motor turning this many degrees: ', degrees)  # Placeholder


def turn(degrees_to_rotate):
    turn_by_x_degrees(degrees_to_rotate)
    print('Turning this many degrees: ', degrees_to_rotate)  # Placeholder


def convert_distance_to_degrees(distance_to_move):
    revolutions = distance_to_move / WHEEL_CIRCUMF_CM
    revolution_degrees = revolutions * 360
    return revolution_degrees


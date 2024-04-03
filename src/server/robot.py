import math
import time

from ev3dev2.motor import (OUTPUT_A, OUTPUT_B, OUTPUT_D, MoveTank, SpeedPercent, MediumMotor)

WHEEL_DIMENSION = 5.5
DIST_BETWEEN_WHEELS = 13.5

WHEEL_CIRCUMF_CM = WHEEL_DIMENSION * math.pi
ROBOT_START_X = 10
ROBOT_START_Y = 20
tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

collector_motor = MediumMotor(OUTPUT_B)
collector_motor.reset()
"""
class Robot:

    def __init__(self):
        self.position = np.array([ROBOT_START_X, ROBOT_START_Y], dtype=int)
        self.pivot = 0

    def get_position(self):
        return self.position
"""


def run_collector_clockwise(): collector_motor.on(30)

def stop_motor(): collector_motor.off()


def run_collector_counterclockwise(): collector_motor.on(-30)


# Function to turn the robot by x degrees
def turn_by_x_degrees(degrees):
    degrees_to_turn = (degrees * DIST_BETWEEN_WHEELS) / WHEEL_DIMENSION
    tank_drive.on_for_degrees(SpeedPercent(25), SpeedPercent(-25), degrees_to_turn)


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

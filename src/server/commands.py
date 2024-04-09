import math

from ev3dev2.motor import (OUTPUT_A, OUTPUT_B, OUTPUT_D, MoveTank, SpeedPercent, MediumMotor)

WHEEL_DIMENSION = 5.5
DIST_BETWEEN_WHEELS = 13.5

WHEEL_CIRCUMF_CM = WHEEL_DIMENSION * math.pi
ROBOT_START_X = 10
ROBOT_START_Y = 20


class Commands:
    def __init__(self):
        self.tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
        self.collector_motor = MediumMotor(OUTPUT_B)
        self.collector_motor.reset()

    def run_collector_clockwise(self): self.collector_motor.on(30)

    def stop_motor(self): self.collector_motor.off(brake=True)

    def run_collector_counterclockwise(self): self.collector_motor.on(-30)

    # Function to turn the robot by x degrees
    def turn_by_x_degrees(self, degrees):
        self.collector_motor.off()
        motor_revolutions = (degrees * DIST_BETWEEN_WHEELS) / WHEEL_DIMENSION
        self.tank_drive.on_for_degrees(SpeedPercent(25), SpeedPercent(-25), motor_revolutions)

    def drive(self, distance_to_move):
        # revs = get_wheel_revolutions(distance_to_move)
        degrees = convert_distance_to_degrees(distance_to_move)
        self.tank_drive.on_for_degrees(SpeedPercent(30), SpeedPercent(30), degrees)
        print('Wheel motor turning this many degrees: ', degrees)  # Placeholder

    # def turn(degrees_to_rotate):
    #     self.turn_by_x_degrees(degrees_to_rotate)
    #     print('Turning this many degrees: ', degrees_to_rotate)  # Placeholder


def convert_distance_to_degrees(distance_to_move):
    revolutions = distance_to_move / WHEEL_CIRCUMF_CM
    revolution_degrees = revolutions * 360
    return revolution_degrees

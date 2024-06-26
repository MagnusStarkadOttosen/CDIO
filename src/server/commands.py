import math
import time

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

    def stop_collector(self): self.collector_motor.off(brake=True)

    def run_collector_counterclockwise(self):
        self.collector_motor.on(-55)

    # Function to turn the robot by x degrees
    def turn_by_x_degrees(self, degrees):
        """
        Turns the robot by a specified number of degrees.

        Parameters
        ----------
        degrees : float
            The number of degrees to turn the robot.
        """
        self.tank_drive.off()
        motor_revolutions = (degrees * DIST_BETWEEN_WHEELS) / WHEEL_DIMENSION
        self.tank_drive.on_for_degrees(SpeedPercent(25), SpeedPercent(-25), motor_revolutions)
        self.tank_drive.on(SpeedPercent(30), SpeedPercent(30))

    def drive(self, distance_to_move):
        """
        Drives the robot forward by a specified distance.

        Parameters
        ----------
        distance_to_move : float
            The distance to move the robot in centimeters.
        """
        degrees = convert_distance_to_degrees(distance_to_move)
        self.tank_drive.on_for_degrees(SpeedPercent(10), SpeedPercent(10), degrees)
        print('Wheel motor turning this many degrees: ', degrees)

    def drive_backwards(self, distance_to_move):
        """
        Drives the robot backward by a specified distance.

        Parameters
        ----------
        distance_to_move : float
            The distance to move the robot in centimeters.
        """
        degrees = convert_distance_to_degrees(distance_to_move)
        self.tank_drive.on_for_degrees(SpeedPercent(-10), SpeedPercent(-10), degrees)
        print('Wheel motor turning this many degrees: ', degrees)

    def drive_inf(self,speed):
        """
        Drives the robot indefinitely at a specified speed. Forward or backwards depending on positive or negative speed

        Parameters
        ----------
        speed : int
            The speed at which to drive the robot.
        """
        self.tank_drive.on(SpeedPercent(speed), SpeedPercent(speed))

    def drive_back(self):
        self.tank_drive.on(SpeedPercent(-10), SpeedPercent(-10))

    def stop(self):
        """
        Stops the robot.
        """
        self.tank_drive.off()

    def turn_left(self, speed):
        """
        Turns the robot left at a specified speed.
        Or turns the robot right if given negative speed

        Parameters
        ----------
        speed : int
            The speed at which to turn the robot.
        """
        self.tank_drive.on(speed, -speed)

    def comment(self, text):
        print(text)


def convert_distance_to_degrees(distance_to_move):
    """
    Converts a distance to the corresponding number of degrees the wheel motors need to turn.

    Parameters
    ----------
    distance_to_move : float
        The distance to move the robot in centimeters.

    Returns
    -------
    float
        The number of degrees the wheel motors need to turn.
    """
    revolutions = distance_to_move / WHEEL_CIRCUMF_CM
    revolution_degrees = revolutions * 360
    return revolution_degrees

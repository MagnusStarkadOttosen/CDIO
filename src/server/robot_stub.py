import math
from src.server.robot import convert_distance_to_degrees
WHEEL_DIMENSION = 5.5
DIST_BETWEEN_WHEELS = 13.5

WHEEL_CIRCUMF_CM = WHEEL_DIMENSION * math.pi


class RobotStub:
    @staticmethod
    def run_collector_clockwise(): print("Collector motor is on clockwise")

    @staticmethod
    def run_collector_counterclockwise(): print("Collector motor is on counterclockwise")

    @staticmethod
    def stop_collector(): print("Stopping motor")

    # Function to turn the robot by x degrees
    @staticmethod
    def turn_by_x_degrees(degrees):
        motor_revolutions = (degrees * DIST_BETWEEN_WHEELS) / WHEEL_DIMENSION
        print(f"Turning robot by {motor_revolutions} degrees")

    @staticmethod
    def drive(distance_to_move):
        # revs = get_wheel_revolutions(distance_to_move)
        degrees = convert_distance_to_degrees(distance_to_move)
        print('Wheel motor turning this many degrees: ', degrees)  # Placeholder

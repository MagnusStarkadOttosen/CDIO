import math

WHEEL_DIMENSION = 5.5
DIST_BETWEEN_WHEELS = 13.5

WHEEL_CIRCUMF_CM = WHEEL_DIMENSION * math.pi

class RobotStub:

    def run_collector_clockwise(self): print("Collector motor is on clockwise")


    def run_collector_counterclockwise(self): print("Collector motor is on counterclockwise")


    def stop_motor(self): print("Stopping motor")


    # Function to turn the robot by x degrees
    def turn_by_x_degrees(self, degrees):
        degrees_to_turn = (degrees * DIST_BETWEEN_WHEELS) / WHEEL_DIMENSION
        print(f"Turning robot by {degrees_to_turn} degrees")


    def drive(self, distance_to_move):
        # revs = get_wheel_revolutions(distance_to_move)
        degrees = self.convert_distance_to_degrees(distance_to_move)
        print('Wheel motor turning this many degrees: ', degrees)  # Placeholder

    def convert_distance_to_degrees(self,distance_to_move):
        revolutions = distance_to_move / WHEEL_CIRCUMF_CM
        revolution_degrees = revolutions * 360
        return revolution_degrees

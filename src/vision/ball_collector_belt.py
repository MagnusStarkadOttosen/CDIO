from ev3dev2.motor import MediumMotor, OUTPUT_A, SpeedPercent
from time import sleep

class Collector:
    def __init__(self, motor_port=OUTPUT_A):
        """Initialize the conveyor belt with a motor connected to the specified port."""
        self.motor = MediumMotor(motor_port)
        self.motor.reset()

    def motor_on(self, speed_pct):
        """Turns the motor on with the given speed percentage."""
        self.motor.on(SpeedPercent(speed_pct))

    def motor_off(self):
        """Turns the motor off."""
        self.motor.off()

    def move_clockwise(self, speed_pct=30, duration=1.0):
        """Moves the conveyor belt clockwise with specified speed and duration."""
        self.motor_on(speed_pct)
        sleep(duration)
        self.motor_off()

    def move_anticlockwise(self, speed_pct=30, duration=1.0):
        """Moves the conveyor belt anticlockwise with specified speed and duration."""
        self.motor_on(-speed_pct)  # Negative speed for reverse direction
        sleep(duration)
        self.motor_off()

    def stop_belt(self):
        """Stops the conveyor belt."""
        self.motor_off()

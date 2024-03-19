from ev3dev2.motor import MediumMotor, OUTPUT_A, SpeedPercent
from time import sleep

class Grabber:
    def __init__(self, motor_port=OUTPUT_A):
        """Initialize the grabber with a motor connected to the specified port."""
        self.motor = MediumMotor(motor_port)
        self.motor.reset()

    def open(self, speed_pct=30, duration=0.5):
        """Opens the grabber with specified speed and duration."""
        self.motor.on(SpeedPercent(speed_pct))
        sleep(duration)
        self.motor.off(brake=False)

    def close(self, speed_pct=30, duration=0.5):
        """Closes the grabber with specified speed and duration."""
        self.motor.on(SpeedPercent(-speed_pct))  # Negative speed for reverse direction
        sleep(duration)
        self.motor.off(brake=False)

    def hold(self, position, speed_pct=30):
        """Holds the grabber at a specific position using a given speed."""
        self.motor.run_to_abs_pos(position_sp=position, speed_sp=speed_pct)
        self.motor.wait_while('running')

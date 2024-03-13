#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_D, SpeedPercent
from time import sleep

# Set up the motor on output D
motor = LargeMotor(OUTPUT_D)

# Run the motor at 50% speed for 3 seconds
motor.on_for_seconds(SpeedPercent(50), 3)

# Alternatively, to run the motor indefinitely at 75% speed (until you stop it):
# motor.on(SpeedPercent(75))

# Wait a bit so you can see what's happening
sleep(1)

# Stop the motor, if it's not already stopped
motor.off()
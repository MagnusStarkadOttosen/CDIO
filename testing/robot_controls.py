from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D, SpeedPercent
from ev3dev2._platform.ev3 import INPUT_2, INPUT_1


tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
def drive():
    tank_drive.on(SpeedPercent(30), SpeedPercent(30))

def stop():
    tank_drive.stop()


def move(distance):
    tank_drive.on_for_degrees(SpeedPercent(40), SpeedPercent(40),distance)
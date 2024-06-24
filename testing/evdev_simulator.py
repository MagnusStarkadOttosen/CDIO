#!/usr/bin/env python3

from ev3dev2._platform.ev3 import INPUT_2, OUTPUT_A, OUTPUT_D
from ev3dev2.motor import SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor

# tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
cs = ColorSensor(INPUT_2)


def drive():
    tank_drive.on(SpeedPercent(30), SpeedPercent(30))


def move(distance):
    tank_drive.on_for_degrees(SpeedPercent(40), SpeedPercent(40), distance)


def stop():
    tank_drive.stop()


drive()
tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

while True:
    # avoid_hit_walls()
    if cs.color != 6:
        stop()
        # move_robot_distance(-100)
        #
        # #get_wheel_rotation(30)
        # #tank_drive.on_for_rotations(SpeedPercent(-35), SpeedPercent(-35), 1)
        #
        tank_drive.on_for_degrees(SpeedPercent(40), SpeedPercent(-10), 300)
        # distance = move_robot_distance(300)
        # tank_drive.on_for_degrees(SpeedPercent(30), SpeedPercent(30), distance)
        drive()
        stop()
        #
        # #tank_drive.on_for_rotations(SpeedPercent(20),SpeedPercent(20))
        # #get_distance_to_move(60)

    # drive()

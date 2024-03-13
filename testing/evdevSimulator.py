#!/usr/bin/env python3
from ev3dev2._platform.ev3 import INPUT_2
from ev3dev2.sensor.lego import ColorSensor
from src.vision.wheel_movement import get_wheel_rotation, get_distance_to_move, move_robot_distance
from ev3dev2.sensor.lego import UltrasonicSensor
from src.vision.avoid_hit_walls import avoid_hit_walls
from src.vision.robot_controls import drive



# tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
cs = ColorSensor(INPUT_2)

drive()
while True:
    avoid_hit_walls()
    #if cs.color != 6:
        # tank_drive.stop()
        # move_robot_distance(-100)
        #
        # #get_wheel_rotation(30)
        # #tank_drive.on_for_rotations(SpeedPercent(-35), SpeedPercent(-35), 1)
        #
        # tank_drive.on_for_degrees(SpeedPercent(40), SpeedPercent(-10), 300)
        # distance = move_robot_distance(300)
        # tank_drive.on_for_degrees(SpeedPercent(30), SpeedPercent(30), distance)
        # drive()
        # tank_drive.stop()
        #
        # #tank_drive.on_for_rotations(SpeedPercent(20),SpeedPercent(20))
        # #get_distance_to_move(60)

    #drive()
#!/usr/bin/env python3

from ev3dev2.motor import (MoveTank, OUTPUT_A
, OUTPUT_D, SpeedPercent)
tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
tank_drive.on_for_seconds(SpeedPercent(30), SpeedPercent(30), 2)
tank_drive.on_for_seconds(SpeedPercent(-30), SpeedPercent(-30), 2)




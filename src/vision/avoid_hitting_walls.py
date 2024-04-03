from ev3dev2 import DeviceNotFound
from ev3dev2._platform.ev3 import INPUT_2, INPUT_1, OUTPUT_A, OUTPUT_D
from ev3dev2.motor import MoveTank
from ev3dev2.sensor import Sensor
from ev3dev2.sensor.lego import UltrasonicSensor
from src.vision.robot_controls import stop


WIDTH= 180
HIGHT = 120
SAFE_DISTANCE = 10

try:
    ultrasonic_sensor = UltrasonicSensor(INPUT_2)
    ultrasonic_sensor.mode = 'US-DIST-CM'
    tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

    def avoid_hit_walls():
        while True:
            distance_to_wall = ultrasonic_sensor.distance_centimeters
            if distance_to_wall < SAFE_DISTANCE:
                stop()
            pass
except DeviceNotFound as e:
    print(f"Ultrasonic Sensor not found on {INPUT_1}: {e}")
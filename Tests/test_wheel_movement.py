import unittest
from src.vision.wheel_movement import wheel_rotation, WHEEL_DIMENSION, DISTANCE_TO_MOVE
import math
import sys
sys.path.append('../src')


class TestWheel(unittest.TestCase):
    def test_wheel_rotation(self):
        expected_degrees = (DISTANCE_TO_MOVE / (math.pi * WHEEL_DIMENSION)) * 360
        self.assertAlmostEqual(wheel_rotation(), expected_degrees)
        print('Expectet degree: ' , expected_degrees)


if __name__ == '__main__':
    unittest.main()
import unittest
from src.vision.wheel_movement import wheel_rotation, WHEEL_DIMENSION, DISTANCE_TO_MOVE
from src.vision.wheel_movement import get_distance_to_move, Pos
import math
import sys

sys.path.append('../src')


class TestWheel(unittest.TestCase):
    def test_wheel_rotation(self):
        expected_degrees = (DISTANCE_TO_MOVE / (math.pi * WHEEL_DIMENSION)) * 360
        self.assertAlmostEqual(wheel_rotation(), expected_degrees)
        print('Expectet degree: ', expected_degrees)


class TestDistanceCalculator(unittest.TestCase):
    def test_distance_to_move(self):
        expected_distance = 8.1
        pos_robot = Pos(3, 2)
        pos_ball = Pos(7, 9)
        actual_distance = get_distance_to_move(pos_robot, pos_ball)
        self.assertAlmostEqual(actual_distance, expected_distance)



if __name__ == '__main__':
    unittest.main()

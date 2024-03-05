import unittest
from src.vision.wheel_movement import get_distance_to_move, Pos, WHEEL_CIRCUMF_CM, get_wheel_rotation
import math
import sys

sys.path.append('../src')


class TestWheel(unittest.TestCase):
    def test_wheel_rotation(self):
        distance_to_move = 70  # For test
        expected_degrees = (distance_to_move / WHEEL_CIRCUMF_CM) * 360
        self.assertAlmostEqual(get_wheel_rotation(distance_to_move), expected_degrees)
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

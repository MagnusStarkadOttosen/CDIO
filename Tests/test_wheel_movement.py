import sys
import os
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
import unittest
import numpy as np

from src.client.utilities import get_distance
from src.server.commands import Commands, convert_distance_to_degrees, WHEEL_CIRCUMF_CM

import sys

sys.path.append('../src')


# test get_distance_to_move
class TestWheel(unittest.TestCase):
    def test_wheel_rotation(self):
        distance_to_move = 70  # For test
        expected_degrees = (distance_to_move / WHEEL_CIRCUMF_CM) * 360
        actual_degrees = convert_distance_to_degrees(distance_to_move)
        self.assertAlmostEqual(expected_degrees, actual_degrees)
        print('Expected degree: ', expected_degrees, 'Actual: ', actual_degrees)


class TestDistanceCalculator(unittest.TestCase):
    def test_distance_to_move_negative_vector(self):
        expected_distance = 8.1
        pos_robot = np.array([3, 2], dtype=int)  # Pos(3, 2)
        pos_ball = np.array([7, 9], dtype=int)  # Pos(7, 9)
        actual_distance = get_distance(pos_robot, pos_ball)
        print(actual_distance)
        self.assertAlmostEqual(actual_distance, expected_distance)
        print('Expected distance: ', expected_distance)

    def test_distance_to_move_positive_vector(self):
        expected_distance = 8.1
        pos_robot = np.array([7, 9], dtype=int)  # Pos(5, 2)
        pos_ball = np.array(([3, 2]), dtype=int)  # Pos(7, 9)
        actual_distance = get_distance(pos_robot, pos_ball)
        print(actual_distance)
        self.assertAlmostEqual(actual_distance, expected_distance)
        print('Expected distance: ', expected_distance)

# test get_degrees_to_rotation
class TestRobotRotationCalculator(unittest.TestCase):
    def test_robot_rotation(self):
        robot = Commands()
        robot.M = (0, 0)
        robot.B = (0, 5)
        pos_ball = Pos(5, 5)
        expected_rotation = -45
        actual_rotation = get_degrees_to_rotation(robot, pos_ball)
        self.assertAlmostEqual(actual_rotation, expected_rotation)
        print('Expected rotation: ', expected_rotation)


if __name__ == '__main__':
    unittest.main()

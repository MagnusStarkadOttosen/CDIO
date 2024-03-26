import sys
import os
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
import unittest
from src.vision.wheel_movement import get_distance_to_move, WHEEL_CIRCUMF_CM, get_wheel_rotation
from src.vision.shape_detection import Pos, Robot

import sys

sys.path.append('../src')



# test get_distance_to_move

class TestDistanceCalculator(unittest.TestCase):
    def test_distance_to_move(self):
        expected_distance = 8.1
        pos_robot = Pos(3, 2)
        pos_ball = Pos(7, 9)
        actual_distance = get_distance_to_move(pos_robot, pos_ball)
        self.assertAlmostEqual(actual_distance, expected_distance)
        print('Expected distance: ', expected_distance)

    def test_distance_to_move_negative(self):
        expected_distance = 7.3
        pos_robot = Pos(5, 2)
        pos_ball = Pos(7, 9)
        actual_distance = get_distance_to_move(pos_robot, pos_ball)
        self.assertAlmostEqual(actual_distance, expected_distance)
        print('Expected distance: ', expected_distance)

# test get_degrees_to_rotation
class TestRobotRotationCalculator(unittest.TestCase):
    def test_robot_rotation(self):
        robot = Robot()
        robot.M = (0, 0)
        robot.B = (0, 5)
        pos_ball = Pos(5, 5)
        expected_rotation = -45
        actual_rotation = get_wheel_rotation(robot, pos_ball)
        self.assertAlmostEqual(actual_rotation, expected_rotation)
        print('Expected rotation: ', expected_rotation)


if __name__ == '__main__':
    unittest.main()

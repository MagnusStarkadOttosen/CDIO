import unittest
from src.vision.wheel_movement import get_distance_to_move
from src.server.robot import Pos, Robot, get_wheel_revolutions, WHEEL_CIRCUMF_CM

import sys

sys.path.append('../src')


class TestWheel(unittest.TestCase):
    def test_wheel_rotation(self):
        distance_to_move = 70  # For test
        expected_degrees = (distance_to_move / WHEEL_CIRCUMF_CM) * 360
        actual_degrees = get_wheel_revolutions(distance_to_move)
        self.assertAlmostEqual(expected_degrees, actual_degrees)
        print('Expected degree: ', expected_degrees, 'Actual: ', actual_degrees)


class TestDistanceCalculator(unittest.TestCase):
    def test_distance_to_move(self):
        expected_distance = 8.1
        pos_robot = Pos(3, 2)
        pos_ball = Pos(7, 9)
        actual_distance = get_distance_to_move(pos_robot, pos_ball)
        self.assertAlmostEqual(actual_distance, expected_distance)

    def test_distance_to_move_negative(self):
        expected_distance = 7.3
        pos_robot = Pos(5, 2)
        pos_ball = Pos(7, 9)
        actual_distance = get_distance_to_move(pos_robot, pos_ball)
        self.assertAlmostEqual(actual_distance, expected_distance)


# NOT DONE!
class TestRobotRotationCalculator(unittest.TestCase):
    def test_robot_rotation(self):
        robot = Robot()
        expected_degrees = 3
        pos_ball = Pos(7, 9)


if __name__ == '__main__':
    unittest.main()

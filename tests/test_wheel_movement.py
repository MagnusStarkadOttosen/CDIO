import math
import unittest
#from src.vision.wheel_movement import get_distance_to_move, WHEEL_CIRCUMF_CM, get_wheel_rotation, get_degrees_to_turn
#from src.vision.shape_detection import Pos, Robot

import sys

sys.path.append('../src')
from src.vision.wheel_movement import get_distance_to_move, WHEEL_CIRCUMF_CM, get_wheel_rotation, get_degrees_to_turn
from src.vision.shape_detection import Pos, Robot


class TestWheel(unittest.TestCase):
    def test_wheel_rotation(self):
        distance_to_move = 70  # For test
        expected_degrees = (distance_to_move / WHEEL_CIRCUMF_CM) * 360
        self.assertAlmostEqual(get_wheel_rotation(distance_to_move), expected_degrees)
        print('Expected degree: ', expected_degrees)


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


class TestRobotRotationCalculator(unittest.TestCase):
    def test_robot_rotation(self):
        robot = Robot()
        expected_degrees = 3
        pos_ball = Pos(7, 9)
        #actual_degrees = get_degrees_to_pivot(robot.pivot, pos_ball)

class TestRobotTurn(unittest.TestCase):
    def test_robot_turn(self):
        robot = Robot()
        robot.pivot =0
        expected_degrees =60.94539590092285
        pos_ball = Pos(5, 9)
        actual_degrees = get_degrees_to_turn(target_pos= pos_ball)
        self.assertAlmostEqual(actual_degrees, expected_degrees)

if __name__ == '__main__':
    unittest.main()


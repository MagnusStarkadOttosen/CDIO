import sys
import os
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
import unittest
from src.vision.wheel_movement import get_distance_to_move
from src.vision.shape_detection import Pos, Robot
from src.vision.wheel_movement import get_degrees_to_rotation


# test get_distance_to_move
class TestDistanceCalculator(unittest.TestCase):
    def test_distance_to_move(self):
        robot = Robot()
        robot.M = (3, 2)
        robot.B = (7, 9)
        expected_distance = 8.06
        actual_distance = get_distance_to_move(robot, robot.B)
        self.assertAlmostEqual(actual_distance, expected_distance)
        print('Expected distance: ', expected_distance)

    def test_distance_to_move_negative(self):
        robot = Robot()
        robot.M = (5, 2)
        robot.B = (7, 9)
        expected_distance = 7.28
        actual_distance = get_distance_to_move(robot, robot.B)
        self.assertAlmostEqual(actual_distance, expected_distance)
        print('Expected distance: ', expected_distance)

# test get_degrees_to_rotation
class TestRobotRotationCalculator(unittest.TestCase):
    def test_robot_rotation(self):
        robot = Robot()
        robot.M = (0, 0)
        robot.B = (5,5 )
        target_pos = (0, 14)
        expected_degrees = 45
        actual_degrees = get_degrees_to_rotation(robot,target_pos)
        self.assertAlmostEqual(actual_degrees, expected_degrees)
        print('Expected degree: ', expected_degrees)

if __name__ == '__main__':
    unittest.main()

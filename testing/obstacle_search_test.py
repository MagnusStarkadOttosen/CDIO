import unittest
from unittest.mock import patch
import sys
import os

from client.search_targetpoint.obstacle_search import obstacle_Search
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

mock_midpoint = [900, 600]

class TestObstacleSearch(unittest.TestCase):

    @patch('client.vision.shape_detection.detect_obstacles', return_value=([], mock_midpoint))
    def test_obstacle_search(self, mock_detect_obstacles):
        ball_dot = [680, 600]
        result = obstacle_Search(ball_dot, 0, 1, mock_midpoint)
        expected_result = [810, 330]  # [900 - 90, 600 - 270]
        self.assertEqual(result, expected_result, "Failed for ball_dot = [680, 600]")

        ball_dot = [680, 800]
        result = obstacle_Search(ball_dot, 0, 1, mock_midpoint)
        expected_result = [810, 870]  # [900 - 90, 600 + 270]
        self.assertEqual(result, expected_result, "Failed for ball_dot = [680, 800]")

        ball_dot = [840, 800]
        result = obstacle_Search(ball_dot, 0, 1, mock_midpoint)
        expected_result = [990, 870]  # [900 + 90, 600 + 270]
        self.assertEqual(result, expected_result, "Failed for ball_dot = [840, 800]")

        ball_dot = [840, 600]
        result = obstacle_Search(ball_dot, 0, 1, mock_midpoint)
        expected_result = [990, 330]  # [900 + 90, 600 - 270]
        self.assertEqual(result, expected_result, "Failed for ball_dot = [840, 600]")

if __name__ == '__main__':
    unittest.main()

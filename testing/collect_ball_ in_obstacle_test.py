import unittest
from unittest.mock import patch, MagicMock
import cv2
import numpy as np

import mainloop

class TestRobotReactionToObstacle(unittest.TestCase):
    def setUp(self):
        self.main_loop = mainloop()

    def load_image(self, filepath):
        return cv2.imread(filepath)

    @patch('src.client.vision.camera.cv2.VideoCapture.read')
    @patch('src.client.vision.shape_detection.detect_robot')
    @patch('src.client.vision.filters.filter_image')
    @patch('src.client.vision.shape_detection.detect_balls')
    @patch('src.client.vision.shape_detection.detect_obstacles')
    @patch('src.client.search_targetpoint.obstacle_search.obstacle_Search')
    @patch('src.client.search_targetpoint.obstacle_search.is_ball_in_obstacle')
    def test_robot_reacts_to_obstacle(self, mock_is_ball_in_obstacle, mock_obstacle_search, mock_detect_obstacles, mock_detect_balls, mock_filter_image, mock_detect_robot, mock_cv2_read):
       
        image = self.load_image('path_to_your_real_image.jpg')

     
        
       
        expected_calls = [
            patch('self.main_loop.client.send_command').call("start_collect"),
            patch('self.main_loop.client.send_command').call("move 7"),
            patch('self.main_loop.client.send_command').call("move -7"),
            patch('self.main_loop.client.send_command').call("stop_collect"),
            patch('self.main_loop.client.send_command').call("stop")
        ]
        
        self.main_loop.client.send_command.assert_has_calls(expected_calls, any_order=True)

if __name__ == '__main__':
    unittest.main()

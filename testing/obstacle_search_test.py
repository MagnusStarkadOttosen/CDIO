import unittest
from unittest.mock import patch
import sys
import os


def obstacle_Search(ball_dot, i, j, midpoint):
    target_point = [0, 0]
    if ball_dot[i] < midpoint[i] and ball_dot[j] < midpoint[j]:
        target_point = [midpoint[0] - 95, midpoint[1] - 320]  
        target=   [midpoint[0] - 95, midpoint[1] + 320]  
    elif ball_dot[i] < midpoint[i] and ball_dot[j] > midpoint[j]:
        target_point = [midpoint[0] - 95, midpoint[1] + 320]  
        target=   [midpoint[0] - 95, midpoint[1] - 320]     
    elif ball_dot[i] > midpoint[i] and ball_dot[j] > midpoint[j]:
        target_point = [midpoint[0] + 95, midpoint[1] + 320] 
        target=   [midpoint[0] + 95, midpoint[1] - 320]       
    elif ball_dot[i] > midpoint[i] and ball_dot[j] < midpoint[j]:
        target_point = [midpoint[0] + 95, midpoint[1] - 320]   
        target=   [midpoint[0] + 95, midpoint[1] + 320]   
    return target_point


class TestObstacleSearch(unittest.TestCase):
    mock_midpoint = [900, 600]
   
    def test_obstacle_search(self):
        ball_dot = [880, 570]
        target_point = obstacle_Search(ball_dot, 0, 1, self.mock_midpoint)
        self.assertEqual(target_point, [805, 280])

        ball_dot = [880, 630]
        target_point = obstacle_Search(ball_dot, 0, 1, self.mock_midpoint)
        self.assertEqual(target_point, [805, 920])

        ball_dot = [980, 570]
        target_point = obstacle_Search(ball_dot, 0, 1, self.mock_midpoint)
        self.assertEqual(target_point, [995, 280])

        ball_dot = [980, 630]
        target_point = obstacle_Search(ball_dot, 0, 1, self.mock_midpoint)
        self.assertEqual(target_point, [995, 920])
        
       

if __name__ == '__main__':
    unittest.main()

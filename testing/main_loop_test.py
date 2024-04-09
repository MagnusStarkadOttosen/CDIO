import cv2
import unittest

from src.client.field.robot import calc_degrees_to_rotate
from src.client.vision.shape_detection import detect_balls, detect_robot


class TestMainLoop(unittest.TestCase):
    def run_main_loop(self):
        image_name = "robot_ball_90.jpeg"
        image = cv2.imread('images/' + image_name)

        robot_pos = detect_robot(image)
        balls = detect_balls(image)
        degrees_to_rotate = calc_degrees_to_rotate(robot_pos
                                                   )

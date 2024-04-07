import unittest

import cv2

from src.client.vision.shape_detection import detect_balls
from testing.image_generation import write_image_to_file
from src.client.vision.filters import filter_image_red, filter_image_green


class TestBallDetection(unittest.TestCase):
    def test_detect_balls(self):
        image_name = "three_balls_extra_skewed.jpg"
        image = cv2.imread('images/' + image_name)
        balls = detect_balls(image)
        print_image(image, balls, image_name)

    def test_detect_red_dot(self):
        image_name = 'image_with_robot.jpeg'
        image = cv2.imread('images/' + image_name)
        balls = detect_balls(filter_image_red(image))
        print_image(image, balls, image_name)


def print_image(image, balls, image_name):
    if balls is not None:
        idx = 0
        for ball in balls:
            # print(f"{type(ball[0])},type({ball[1]}),type({ball[2]})")
            # Draw the outer circle
            cv2.circle(image, (ball[0], ball[1]), ball[2], (128, 0, 128), 2)
            # Draw the center of the circle
            cv2.circle(image, (ball[0], ball[1]), 2, (128, 0, 128), 3)
            # Enumerate the detected balls
            cv2.putText(image, str(idx), (ball[0], ball[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            idx += 1
            print("ball x:", ball[0], "y:", ball[1])

        write_image_to_file('circles_detected_' + image_name, image)
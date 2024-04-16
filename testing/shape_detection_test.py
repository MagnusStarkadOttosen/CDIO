import unittest

import cv2

from src.client.vision.shape_detection import detect_balls
from testing.image_generation import write_image_to_file
from src.client.vision.filters import filter_image_red, filter_image_green, filter_image_by_color



class TestBallDetection(unittest.TestCase):
    def test_detect_balls_vector_drawing(self):
        image_name = "three_balls_extra_skewed.jpg"
        image = cv2.imread('images/' + image_name)
        balls = detect_balls(image, max_radius=25)
        ball_count = 0 if balls is None else len(balls)
        print_image(image, balls, image_name)
        self.assertEqual(ball_count, 3)

    def test_detect_balls_real_img(self):
        image_name = "1.jpg"
        image = cv2.imread('images/' + image_name)
        balls = detect_balls(image)
        ball_count = 0 if balls is None else len(balls)
        print_image(image, balls, image_name)
        self.assertEqual(ball_count, 0)  # expect 0 because circles too large

    def test_detect_9_balls(self):
        image_name = "9_balls_on_field.jpeg"
        image = cv2.imread('images/' + image_name)
        balls = detect_balls(image)
        ball_count = 0 if balls is None else len(balls)
        print_image(image, balls, image_name)
        self.assertEqual(ball_count, 9)

    def test_detect_1_ball(self):
        image_name = "robot_ball_90.jpeg"
        image = cv2.imread('images/' + image_name)
        balls = detect_balls(image, min_radius=20)
        ball_count = 0 if balls is None else len(balls)
        print_image(image, balls, image_name)
        self.assertEqual(ball_count, 1)

    def test_detect_red_dot(self):
        image_name = 'robot_ball_90.jpeg'
        image = cv2.imread('images/' + image_name)
        balls = detect_balls(filter_image_by_color(image, "red"),
                             min_radius=25, max_radius=35)
        ball_count = 0 if balls is None else len(balls)
        print_image(image, balls, 'red_' + image_name)
        self.assertEqual(ball_count, 1)

    def test_detect_green_dot(self):
        image_name = 'robot_ball_90.jpeg'
        image = cv2.imread('images/' + image_name)
        balls = detect_balls(filter_image_green(image),
                             min_radius=25, max_radius=35)
        ball_count = 0 if balls is None else len(balls)
        print_image(image, balls, 'green_' + image_name)
        self.assertEqual(ball_count, 1)


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
    else:
        print("No balls detected to draw on the image.")

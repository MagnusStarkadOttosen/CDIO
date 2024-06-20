import cv2

from src.client.vision.filters import filter_image_white
from src.client.vision.pathfinder import find_nearest_ball
from src.client.vision.shape_detection import detect_balls, detect_robot


class Field:
    def __init__(self, start_frame):
        self.balls = detect_balls(filter_image_white(start_frame))

    def get_white_ball_loop(self, frame):
        robot_pos, robot_direction = detect_robot(frame,,
        nearest_ball_pos = find_nearest_ball(robot_pos, self.balls)

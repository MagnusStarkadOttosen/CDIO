import time

import cv2
import numpy as np

from src.client.field.coordinate_system import are_points_close, find_corner_points_full, warp_perspective
from src.client.field.field import Field
from src.client.field.robot import calc_vector_direction, calc_degrees_to_rotate
from src.client.pc_client import ClientPC
from src.client.vision.camera import capture_image
from src.client.vision.filters import filter_image_white, filter_image_orange
from src.client.vision.pathfinder import find_nearest_ball
from src.client.vision.shape_detection import detect_balls, detect_robot

WHITE_BALL_COUNT = 10
ROBOT_CAPACITY = 6
TOLERANCE = 1
DST_SIZE = (1200, 1800)


class Main:
    def __init__(self):
        self.client = ClientPC()
        self.balls = None
        self.collect_orange_ball = False
        self.target_pos = None

    def main_loop(self):
        while len(self.balls) > WHITE_BALL_COUNT - ROBOT_CAPACITY - 1:
            self._collect_ball()

        self.collect_orange_ball = True
        while self.collect_orange_ball:
            self._collect_ball()
        self._deliver_balls_loop()

        while len(self.balls) > 0:
            self._collect_ball()
        self._deliver_balls_loop()
        self.client.send_command("stop_collect")

    def _collect_ball(self):  # TODO break up _collect_ball in smaller functions
        capture_image("test.jpg")
        image = cv2.imread("images/capturedImage/test.jpg")
        final_points = find_corner_points_full(image)
        warped_img = warp_perspective(image, final_points, DST_SIZE)

        robot_pos, robot_direction = detect_robot(warped_img)

        # Set target ball position
        if not self.collect_orange_ball:
            self.balls = detect_balls(filter_image_white(warped_img))
            if self.balls is None:
                return
            self.target_pos = find_nearest_ball(robot_pos, self.balls)
        else:
            self.balls = detect_balls(filter_image_orange(warped_img))
            if self.balls is None:
                self.collect_orange_ball = False
                self.balls = detect_balls(filter_image_white(warped_img))
                return
            self.target_pos = (self.balls[0][0], self.balls[0][1])
            self._navigate_to_target(robot_pos, robot_direction)

    def _deliver_balls_loop(self):
        # get angle to turn from current robot direction
        # send command to drive until robot_pos = goal_pos
        self.client.send_command("stop")
        self.client.send_command("deliver")
        time.sleep(5)  # TODO use on_for_degrees in deliver command server-side
        self.client.send_command("start_collect")

    def _navigate_to_target(self, robot_pos, robot_direction):
        # Calculate target direction vector
        target_direction = calc_vector_direction(robot_pos, self.target_pos)

        # Check if robot arrived at target destination
        if are_points_close(robot_pos, self.target_pos):
            self.client.send_command("stop")
            return

        # Calculate the degrees the robot needs to turn to face robot
        deg = calc_degrees_to_rotate(robot_direction, target_direction)

        # Check if angle need to change
        if deg < -TOLERANCE or deg > TOLERANCE:
            self.client.send_command("turn " + deg)
            # self.client.send_command("start_drive")

    def _run_get_white_balls_loop(self, filtered_image):  # probably needs to be video feed here
        self.balls = detect_balls(filtered_image)

    # get_image
    # modify_image
    # update_robot_position
    # plan_path
    # move_robot


def get_image():
    pass


def modify_image(image):
    pass


def update_robot_position():
    pass


def plan_path():
    pass


def move_robot():
    pass

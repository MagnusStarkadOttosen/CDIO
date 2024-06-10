import time
import cv2
import numpy as np

from src.client.field.coordinate_system import are_points_close, find_corner_points_full, warp_perspective
from src.client.field.field import Field
from src.client.field.robot import calc_vector_direction, calc_degrees_to_rotate
from src.client.pc_client import ClientPC
from src.client.vision.camera import capture_image, initialize_camera
from src.client.vision.filters import filter_image_white, filter_image_orange
from src.client.vision.pathfinder import find_nearest_ball
from src.client.vision.shape_detection import detect_balls, detect_robot
from src.client.search_targetpoint.a_star_search import find_path

WHITE_BALL_COUNT = 10
ROBOT_CAPACITY = 6
TOLERANCE = 10
DST_SIZE = (1200, 1800)


def _detect_initial_balls(final_points):
    warped_img = warp_perspective(cv2.imread("images/capturedImage/test.jpg"), final_points, DST_SIZE)
    return detect_balls(warped_img)


class Main:
    def __init__(self):
        self.client = ClientPC()
        self.balls = None
        self.collect_orange_ball = False
        self.target_pos = None
        self.camera = initialize_camera(index=2)
        self.grid = None
        self.robot_is_moving = False
        self.robot_is_turning = False

    def main_loop(self):
        final_points = self._initialize_field()
        self.balls = _detect_initial_balls(final_points)

        self._collect_white_balls(final_points)
        self._collect_and_deliver_orange_ball(final_points)
        self._collect_remaining_balls(final_points)

        self.client.send_command("stop_collect")


    def _initialize_field(self):
        self.grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        ret, frame = self.camera.read()
        final_points = find_corner_points_full(frame, doVerbose=False)
        # capture_image(self.camera, "test.jpg")
        # image = cv2.imread("images/capturedImage/test.jpg")
        # final_points = find_corner_points_full(image)
        return final_points

    def _collect_white_balls(self, final_points):
        while len(self.balls) > WHITE_BALL_COUNT - ROBOT_CAPACITY - 1:
            self._collect_ball(final_points, filter_image_white)

    def _collect_and_deliver_orange_ball(self, final_points):
        self.collect_orange_ball = True
        while self.collect_orange_ball:
            self._collect_ball(final_points, filter_image_orange)
        self._deliver_balls()

    def _collect_remaining_balls(self, final_points):
        while len(self.balls) > 0:
            self._collect_ball(final_points, filter_image_white)
        self._deliver_balls()

    def _collect_ball(self, final_points, filter_image):
        ret, frame = self.camera.read()
        final_points = find_corner_points_full(frame, doVerbose=False)
        warped_img = warp_perspective(frame, final_points, DST_SIZE)

        robot_pos, robot_direction = detect_robot(warped_img)

        if self.collect_orange_ball:
            self.balls = detect_balls(filter_image_orange(warped_img))
            if not self.balls:
                self.collect_orange_ball = False
                return
            self.target_pos = self.balls[0][:2]
        else:
            self.balls = detect_balls(filter_image(warped_img))
            if not self.balls:
                return
            self.target_pos = find_nearest_ball(robot_pos, self.balls) # TODO handle target being null

        path = find_path(self.grid, robot_pos, self.target_pos)
        self._navigate_to_target(robot_pos, robot_direction, path)

    def _deliver_balls(self):
        self.client.send_command("stop")
        self.client.send_command("deliver")
        time.sleep(5)  # TODO use on_for_degrees in deliver command server-side
        self.client.send_command("start_collect")

    def _navigate_to_target(self, robot_pos, robot_direction, path):
        for (x, y) in path:
            while True:
                ret, frame = self.camera.read()
                final_points = find_corner_points_full(frame, doVerbose=False)
                warped_img = warp_perspective(frame, final_points, DST_SIZE)

                robot_pos, robot_direction = detect_robot(warped_img)
                target_direction = calc_vector_direction((x, y), robot_pos)

                if are_points_close(robot_pos, (x, y)):
                    self.client.send_command("stop")
                    self.robot_is_moving = False
                    break

                angle = calc_degrees_to_rotate(robot_direction, target_direction)

                if angle < -TOLERANCE or angle > TOLERANCE:
                    self.robot_is_turning = True
                    print("start rotating")
                    if self.robot_is_moving:
                        self.client.send_command("stop")
                        self.robot_is_moving = False
                    self.client.send_command(f"turn {angle}")

                if angle > -TOLERANCE or angle < TOLERANCE:
                    self.robot_is_turning = False

                if not self.robot_is_moving and not self.robot_is_turning:
                    self.client.send_command("start_drive")
                    self.robot_is_moving = True

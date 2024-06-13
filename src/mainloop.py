import time

import cv2
import numpy as np
from client.search_targetpoint.obstacle_search import is_ball_in_obstacle, obstacle_Search
from src.client.field.collect_from_corner import is_ball_in_corner, check_corners, robot_movement_based_on_corners
from src.client.field.coordinate_system import are_points_close, find_corner_points_full, warp_perspective
# from src.client.field.field import Field
from src.client.field.robot import calc_vector_direction, calc_degrees_to_rotate
from src.client.pathfinding.CalculateCommandList import rotate_vector_to_point
from src.client.pc_client import ClientPC
from src.client.vision.camera import capture_image, initialize_camera
from src.client.vision.filters import filter_image
from src.client.vision.pathfinder import find_nearest_ball
from src.client.vision.shape_detection import detect_balls, detect_obstacles, detect_robot
from src.client.search_targetpoint.a_star_search import find_path
from src.client.hsvLoad import read_hsv_values


WHITE_BALL_COUNT = 10
ROBOT_CAPACITY = 6
TOLERANCE = 10
TURN_SPEED = 3
DST_SIZE = (1200, 1800)
PIVOT_POINTS = [(300, 600), (1500, 600)]
CORNERS = {
    "top_left": (0, 0),
    "bottom_left": (0, 1200),
    "top_right": (1800, 0),
    "bottom_right": (1800, 1200)
}

class MainLoop:
    def __init__(self):
        self.client = ClientPC()
        self.balls = None
        self.collect_orange_ball = False
        self.target_pos = None
        self.camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.final_points = None
        self.grid = None
        self.robot_is_moving = False
        self.robot_is_turning = False
        self.target_found = False
        self.ball_collected = False
        self.at_target = False
        self.direction_color = read_hsv_values("hsv_presets_white.txt")
        self.orange = read_hsv_values("hsv_presets_orange.txt")
        self.pivot_color = read_hsv_values("hsv_presets_white.txt")
        self.red = read_hsv_values("hsv_presets_red.txt")
        self.white = read_hsv_values("hsv_presets_white.txt")

    def start_main_loop(self):
        self.initialize_field()
        self.balls = self._detect_initial_balls()

        self._collect_white_balls()
        self._collect_and_deliver_orange_ball()
        self._collect_remaining_balls()

        self.client.send_command("stop_collect")

    def initialize_field(self):
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
        self.final_points = find_corner_points_full(frame, self.red, doVerbose=True)

    def _detect_obstacles(self):
        ret, frame = self.camera.read()
        warped_img = warp_perspective(frame, self.final_points, DST_SIZE)
        return detect_obstacles(warped_img)
    def _detect_initial_balls(self):
        ret, frame = self.camera.read()
        warped_img = warp_perspective(frame, self.final_points, DST_SIZE)
        return detect_balls(warped_img)

    def _collect_white_balls(self):
        while len(self.balls) > WHITE_BALL_COUNT - ROBOT_CAPACITY - 1:
            self._collect_ball()

    def _collect_and_deliver_orange_ball(self):
        self.collect_orange_ball = True
        while self.collect_orange_ball:
            self._collect_ball()
        self._deliver_balls()

    def _collect_remaining_balls(self):
        while len(self.balls) > 0:
            self._collect_ball()
        self._deliver_balls()

    def _collect_ball(self):
        ret, frame = self.camera.read()
        # final_points = find_corner_points_full(frame, doVerbose=False)
        warped_img = warp_perspective(frame, self.final_points, DST_SIZE)

        robot_pos, robot_direction = detect_robot(warped_img, self.direction_color, self.pivot_color)

        # if filter_image.equals(filter_image_orange):
        if self.collect_orange_ball:
            self.balls = detect_balls(filter_image(warped_img, self.orange))
            if not self.balls:
                self.collect_orange_ball = False
                return
            self.target_pos = self.balls[0][:2]
        else:
            self.balls = detect_balls(filter_image(warped_img, self.white))
            if not self.balls:
                return
            self.target_pos = find_nearest_ball(robot_pos, self.balls) # TODO handle target being null
            print(f"Nearest ball pos : {self.target_pos[0]},{self.target_pos[1]}")

        if is_ball_in_corner(self.balls):
            corner_result = check_corners(self.balls, threshold=50)
            pivot_points, corner_points = robot_movement_based_on_corners(corner_result)
            path = find_path(self.grid, robot_pos, pivot_points)
            self._navigate_to_target(path)
            self.client.send_command("start_collect")
            self._navigate_to_target(corner_points)
            self._navigate_to_target(path)
            self.client.send_command("stop_collect")
            self.client.send_command("stop")
        elif is_ball_in_obstacle(self.balls, midpoint):
            midpoint=self._detect_obstacles()
            target_point = obstacle_Search(self.balls, 0, 1, midpoint)
            target=  obstacle_Search(self.balls, 1, 0, midpoint)
            path= [target_point]
            self._navigate_to_target(path)
            self.client.send_command("start_collect")
            angle = rotate_vector_to_point(robot_pos, robot_direction,target)
            print(f"after robot pos {robot_pos} and direction {robot_direction} and target {target} and angle: {angle}")
            if angle < -TOLERANCE or angle > TOLERANCE:
                self._course_correction(angle, target)
            self.client.send_command("move 7")
            self.client.send_command("move -7")
            self.client.send_command("stop_collect")
            self.client.send_command("stop")
           
        else:
            path = find_path(self.grid, robot_pos, self.target_pos)
            self._navigate_to_target(path)

    def _deliver_balls(self):
        self.client.send_command("stop")
        self.client.send_command("deliver")
        time.sleep(5)  # TODO use on_for_degrees in deliver command server-side
        self.client.send_command("start_collect")

    def _navigate_to_target(self, path):
        for (x, y) in path:
            while True:
                ret, frame = self.camera.read()
                #final_points = find_corner_points_full(frame, doVerbose=False)
                warped_img = warp_perspective(frame, self.final_points, DST_SIZE)
                print(f"orange hsv values: {self.pivot_color}")
                robot_pos, robot_direction = detect_robot(warped_img, self.direction_color, self.pivot_color)
                if robot_pos is None or robot_direction is None:
                    continue
                if are_points_close(robot_pos, (x,y), tolerance=40):
                    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                    self.client.send_command("stop")
                    self.robot_is_moving = False
                    self.at_target = True
                    break

                angle = rotate_vector_to_point(robot_pos, robot_direction, (x, y))

                # angle = calc_degrees_to_rotate(robot_direction, target_direction)
                print(f"after robot pos {robot_pos} and direction {robot_direction} and target {(x, y)} and angle: {angle}")
                if angle < -TOLERANCE or angle > TOLERANCE:
                    print(f"asdsdkjfsdkjfsdkj {angle}")
                    self._course_correction(angle, (x,y))

                # if self.robot_is_turning:
                #     self.robot_is_turning = False
                #     self.client.send_command("stop")

                if not self.robot_is_moving and not self.robot_is_turning:
                    self.client.send_command("start_drive")
                    self.robot_is_moving = True

    def _course_correction(self, angle, target): # TODO read final points only once at start?
        print(f"inside course correction. Angle: {angle}. Tolerance: {TOLERANCE}")
        while angle < -TOLERANCE or angle > TOLERANCE:
            ret, frame = self.camera.read()
            gen_warped_image = warp_perspective(frame, self.final_points, DST_SIZE)
            print(f"pivot_color hsv values: {self.pivot_color}")
            robot_pos, robot_direction = detect_robot(gen_warped_image, self.direction_color, self.pivot_color)
            print(f"in correction robot pos {robot_pos} and direction {robot_direction} and target {target} and angle: {angle}")
            if robot_pos is None or robot_direction is None:
                continue
            angle = rotate_vector_to_point(robot_pos, robot_direction, target)
            print(f"angle: {angle}")
            if not self.robot_is_turning and angle < 0:
                self.robot_is_turning = True
                self.robot_is_moving = False
                self.client.send_command(f"turn_left {-TURN_SPEED}")
            elif not self.robot_is_turning and angle >= 0:
                self.robot_is_turning = True
                self.robot_is_moving = False
                self.client.send_command(f"turn_left {TURN_SPEED}")
            else:
                self.robot_is_turning = False
        self.robot_is_turning = False
        self.client.send_command("stop")
    
    def temp(self):
        ret, frame = self.camera.read()
        warped_img = warp_perspective(frame, self.final_points, DST_SIZE)
        robot_pos, robot_direction = detect_robot(warped_img, self.direction_color, self.pivot_color)
        return robot_pos, robot_direction


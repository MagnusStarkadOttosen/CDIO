import math
import time

import cv2
#import logging
#
# logging.basicConfig(filename='safe_detect_balls.log', filemode='w',
#                     format='%(asctime)s - %(message)s')


from src.client.pathfinding.FindPath import find_path, cell_is_in_dead_zone
from src.client.pathfinding.GenerateNavMesh import GenerateNavMesh, escape_dead_zone
# from src.client.pathfinding.GenerateNavMesh import find_path
from src.client.search_targetpoint.obstacle_search import is_ball_in_obstacle, obstacle_Search
from src.client.field.collect_from_corner import is_ball_in_corner, check_corners, robot_movement_based_on_corners
from src.client.field.coordinate_system import are_points_close, find_corner_points_full, warp_perspective
from src.client.pathfinding.CalculateCommandList import rotate_vector_to_point
from src.client.pc_client import ClientPC
from src.client.utilities import log_balls, log_path
from src.client.vision.filters import filter_image
from src.client.vision.pathfinder import find_nearest_ball
from src.client.vision.shape_detection import detect_balls, detect_obstacles, detect_robot, safe_detect_balls, \
    safe_detect_robot
from src.client.hsvLoad import read_hsv_values

WHITE_BALL_COUNT = 10
ROBOT_CAPACITY = 6
TOLERANCE = 10
TURN_SPEED = 3
QUICK_TURN_SPEED = 9
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
        self.navmesh = None
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
        self._detect_initial_balls()
        # log_balls("Starting collect orange ball")
        # self._collect_and_deliver_orange_ball()
        log_balls("Starting collect white balls")
        self._collect_white_balls()

        self.client.send_command("stop_collect")

    def initialize_field(self):
        # self.grid = [
        #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        #     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #     [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        #     [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        #     [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        #     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        # ]

        ret, frame = self.camera.read()
        self.final_points = find_corner_points_full(frame, self.red, doVerbose=True)
        warped_img = warp_perspective(frame, self.final_points, DST_SIZE)
        red_hsv_values = read_hsv_values('hsv_presets_red.txt')
        self.navmesh = GenerateNavMesh(warped_img, red_hsv_values)

    def _detect_obstacles(self):
        ret, frame = self.camera.read()
        warped_img = warp_perspective(frame, self.final_points, DST_SIZE)
        return detect_obstacles(warped_img)

    def _detect_initial_balls(self):
        ret, frame = self.camera.read()
        # warped_img = warp_perspective(frame, self.final_points, DST_SIZE)
        self.balls = safe_detect_balls(self.camera, self.final_points, DST_SIZE, self.white)

    def _collect_white_balls(self):
        while len(self.balls) > ROBOT_CAPACITY:
            while len(self.balls) > WHITE_BALL_COUNT - ROBOT_CAPACITY:
                self._collect_ball()
            self._deliver_balls()
        self._collect_remaining_balls()

    def _collect_and_deliver_orange_ball(self):
        self.collect_orange_ball = True
        while self.collect_orange_ball:
            self._collect_ball()
        self._deliver_balls()

    def _collect_remaining_balls(self):
        if self.balls is not None:
            while len(self.balls) > 0:
                self._collect_ball()
            self._deliver_balls()

    def _collect_ball(self):
        ret, frame = self.camera.read()
        # final_points = find_corner_points_full(frame, doVerbose=False)
        warped_img = warp_perspective(frame, self.final_points, DST_SIZE)

        robot_pos, robot_direction = safe_detect_robot(self.camera, self.final_points, DST_SIZE, self.white, self.white)
        # while robot_pos is None or robot_direction is None:
        #     robot_pos, robot_direction = detect_robot(warped_img, self.direction_color, self.pivot_color)

        # if filter_image.equals(filter_image_orange):
        if self.collect_orange_ball:
            self.balls = safe_detect_balls(self.camera, self.final_points,
                                           DST_SIZE, self.orange)
            if self.balls is None:
                log_balls("No orange ball")
                self.collect_orange_ball = False
                return
            self.target_pos = self.balls[0][:2]
        else:
            self.balls = safe_detect_balls(self.camera, self.final_points,
                                           DST_SIZE, self.white)
            if self.balls is None or len(self.balls) == 0:
                return
            print(self.balls)
            self.target_pos = find_nearest_ball(robot_pos, self.balls)  # TODO handle target being null
            #logging.warning(self.target_pos)
            log_balls(self.target_pos)

        # old find_corners code
        # if cell_is_in_dead_zone(robot_pos, self.navmesh):
        #     print("front is in deadzone")
        #     log_path("Is in deadzone")
        #     self.client.send_command("move -5")
        #     return

        front_x, front_y = self._calc_robot_front(robot_direction, robot_pos)
        if cell_is_in_dead_zone((int(front_x),int(front_y)), self.navmesh):
            log_balls(f"front pos: {front_x}, {front_y}")
            print("front is in deadzone")
            log_path("front Is in deadzone")
            new_x, new_y = escape_dead_zone(self.navmesh, (int(front_x), int(front_y)))

            angle = rotate_vector_to_point(robot_pos, robot_direction, (900, 600))
            tolerance = 20
            if angle < -tolerance or angle > tolerance:
                self._course_correction(angle, (900, 600), tol=tolerance)

            self.client.send_command("move 10")

            # if new_x and new_y is not None:
            #     self.target_pos = (new_x, new_y)
            # else:
            #     print("New target none")
            # self.client.send_command("move -5")
            #return

        path = find_path(self.navmesh, warped_img, robot_pos, self.target_pos)
        self._navigate_to_target(path)


    def _calc_robot_front(self, robot_direction, robot_pos):
        # Calculate the magnitude of the direction vector
        magnitude = math.sqrt(robot_direction[0] ** 2 + robot_direction[1] ** 2)

        if magnitude == 0:
            raise ValueError("Direction vector magnitude is zero, cannot move")

        # Calculate the unit direction vector components
        unit_a = robot_direction[0] / magnitude
        unit_b = robot_direction[1] / magnitude

        distance = 5
        # Calculate the new point
        new_x = robot_pos[0] + distance * unit_a
        new_y = robot_pos[1] + distance * unit_b
        return new_x, new_y


    def _collect_ball_in_corner(self, ball_pos, robot_pos, warped_img):
        corner_result = check_corners(ball_pos, threshold=50)
        pivot_points, corner_points = robot_movement_based_on_corners(corner_result)
        path = find_path(warped_img, robot_pos, pivot_points)
        self._navigate_to_target(path)
        self.client.send_command("start_collect")
        self._navigate_to_target(corner_points)
        self._navigate_to_target(path)
        self.client.send_command("stop_collect")
        self.client.send_command("stop")

    def _deliver_balls(self):
        ret, frame = self.camera.read()
        # final_points = find_corner_points_full(frame, doVerbose=False)
        warped_img = warp_perspective(frame, self.final_points, DST_SIZE)
        print(f"orange hsv values: {self.pivot_color}")

        robot_pos, robot_direction = detect_robot(warped_img, self.direction_color, self.pivot_color)
        while robot_pos is None or robot_direction is None:
            robot_pos, robot_direction = detect_robot(warped_img, self.direction_color, self.pivot_color)

        # path_to_goal_A = []
        goal_A_pivot_point = (150, 600)

        # path_to_goal_A.append(goal_A_pivot_point)

        path = find_path(self.navmesh, warped_img, robot_pos, goal_A_pivot_point)

        # path_to_goal_A.append(goal_A_point)
        self.client.send_command("stop_collect")
        self._navigate_to_target(path)

        angle = rotate_vector_to_point(robot_pos, robot_direction, (-100, 600))

        # angle = calc_degrees_to_rotate(robot_direction, target_direction)
        print(
            f"after robot pos {robot_pos} and direction {robot_direction} and target {(-100, 600)} and angle: {angle}")
        if angle < -1 or angle > 1:
            #print(f"asdsdkjfsdkjfsdkj {angle}")
            self._course_correction(angle, (-100, 600), 1)

        self.client.send_command("deliver")
        time.sleep(5)
        self.client.send_command("stop_collect")

    def _navigate_to_target(self, path):
        for (x, y) in path:
            while True:
                ret, frame = self.camera.read()
                # final_points = find_corner_points_full(frame, doVerbose=False)
                warped_img = warp_perspective(frame, self.final_points, DST_SIZE)
                print(f"orange hsv values: {self.pivot_color}")

                # robot_pos, robot_direction = safe_detect_robot(self.camera, self.final_points, DST_SIZE,
                #                                                self.direction_color, self.pivot_color)
                # while robot_pos is None or robot_direction is None:
                #     robot_pos, robot_direction = safe_detect_robot(warped_img, self.direction_color, self.pivot_color)
                robot_pos = None
                robot_direction = None
                while robot_pos is None or robot_direction is None:
                    ret, frame = self.camera.read()
                    gen_warped_image = warp_perspective(frame, self.final_points, DST_SIZE)
                    robot_pos, robot_direction = detect_robot(gen_warped_image, self.direction_color,
                                                                   self.pivot_color)

                if robot_pos is None or robot_direction is None:
                    continue
                if are_points_close(robot_pos, (x, y), tolerance=40):
                    self.client.send_command("stop")
                    # print(f"{robot_pos}aaa{(x,y)}aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                    self.robot_is_moving = False
                    self.at_target = True
                    break

                angle = rotate_vector_to_point(robot_pos, robot_direction, (x, y))

                # angle = calc_degrees_to_rotate(robot_direction, target_direction)
                print(
                    f"after robot pos {robot_pos} and direction {robot_direction} and target {(x, y)} and angle: {angle}")
                tolerance = 10
                if angle < -tolerance or angle > tolerance:
                    print(f"asdsdkjfsdkjfsdkj {angle}")
                    self._course_correction(angle, (x, y), tol=tolerance)

                # if self.robot_is_turning:
                #     self.robot_is_turning = False
                #     self.client.send_command("stop")

                if not self.robot_is_moving and not self.robot_is_turning:
                    self.client.send_command("start_drive 10")
                    self.robot_is_moving = True

                if self.robot_is_moving:
                    if are_points_close(robot_pos, (x, y), 300):
                        self.client.send_command("start_drive 10")
                    else:
                        self.client.send_command("start_drive 10")

                    if are_points_close(robot_pos, self.target_pos, 300):
                        self.client.send_command("start_collect")
                    else:
                        self.client.send_command("stop_collect")

    def _course_correction(self, angle, target, tol=10):
        print(f"inside course correction. Angle: {angle}. Tolerance: {tol}")
        while angle < -tol or angle > tol:
            ret, frame = self.camera.read()
            gen_warped_image = warp_perspective(frame, self.final_points, DST_SIZE)
            print(f"pivot_color hsv values: {self.pivot_color}")

            # robot_pos, robot_direction = safe_detect_robot(self.camera, self.final_points, DST_SIZE,
            #                                                self.direction_color, self.pivot_color)

            # robot_pos, robot_direction = detect_robot(gen_warped_image, self.direction_color, self.pivot_color)
            robot_pos = None
            robot_direction = None
            while robot_pos is None or robot_direction is None:
                ret, frame = self.camera.read()
                gen_warped_image = warp_perspective(frame, self.final_points, DST_SIZE)
                robot_pos, robot_direction = detect_robot(gen_warped_image, self.direction_color, self.pivot_color)

            print(
                f"in correction robot pos {robot_pos} and direction {robot_direction} and target {target} and angle: {angle}")
            if robot_pos is None or robot_direction is None:
                continue
            angle = rotate_vector_to_point(robot_pos, robot_direction, target)
            print(f"angle: {angle}")
            if angle > 50 or angle < -50:
                speed = QUICK_TURN_SPEED
            else:
                speed = TURN_SPEED

            if not self.robot_is_turning and angle < 0:
                self.robot_is_turning = True
                self.robot_is_moving = False
                self.client.send_command(f"turn_left {-speed}")
            elif not self.robot_is_turning and angle >= 0:
                self.robot_is_turning = True
                self.robot_is_moving = False
                self.client.send_command(f"turn_left {speed}")
            else:
                self.robot_is_turning = False
        self.robot_is_turning = False
        self.client.send_command("stop")
        print("stop from course correction")

    def temp(self):
        ret, frame = self.camera.read()
        warped_img = warp_perspective(frame, self.final_points, DST_SIZE)
        robot_pos, robot_direction = detect_robot(warped_img, self.direction_color, self.pivot_color)
        return robot_pos, robot_direction

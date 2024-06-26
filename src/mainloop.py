import math
import time

import cv2

from src.CONSTANTS import GRID_SIZE

from src.client.pathfinding.FindPath import find_path, pretty_print_navmesh
from src.client.pathfinding.GenerateNavMesh import GenerateNavMesh, coordinate_to_cell
from src.client.field.collect_from_corner import ball_is_in_corner, check_corners, \
    get_pivot
from src.client.field.coordinate_system import are_points_close, find_corner_points_full, warp_perspective
from src.client.pathfinding.CalculateCommandList import rotate_vector_to_point
from src.client.pc_client import ClientPC
from src.client.utilities import log_path
from src.client.vision.AIBallDetection import detect_balls_with_model
from src.client.vision.pathfinder import find_nearest_ball
from src.client.vision.shape_detection import detect_obstacles, detect_robot, safe_detect_balls, \
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
        self.camera = cv2.VideoCapture(2, cv2.CAP_DSHOW)
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
        self.white_balls = None
        self.orange_balls = None
        self.tempdeadbool = True

    def start_main_loop(self):
        """
        Starts the main loop, initializes the field, detects initial balls, and handles ball collection and delivery.
        """
        self.initialize_field()
        self._detect_initial_balls_ai()
        self._collect_and_deliver_orange_ball()
        self._collect_white_balls()
        self.client.send_command("stop_collect")

    def initialize_field(self):
        """
        Initializes the field by detecting the corners and generating the navigation mesh.
        """
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
        self.balls = safe_detect_balls(self.camera, self.final_points, DST_SIZE, self.white)


    def _detect_initial_balls_ai(self):
        if True:
            self.tempbool = True
            ret, frame = self.camera.read()
            warped_img = warp_perspective(frame, self.final_points, DST_SIZE)
            self.white_balls, self.orange_balls = detect_balls_with_model(warped_img)
            
            center_x = DST_SIZE[1] / 2
            center_y = DST_SIZE[0] / 2

            def distance_from_center(ball):
                x, y, _ = ball
                return math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            # Filter out the white balls within the specified radius
            self.white_balls = [ball for ball in self.white_balls if distance_from_center(ball) > 200]

    def _collect_white_balls(self):
        """
        Collects white balls until the robot's capacity is reached.
        """
        while len(self.white_balls) > ROBOT_CAPACITY:
            while len(self.white_balls) > WHITE_BALL_COUNT - ROBOT_CAPACITY + 1:
                self._collect_ball()
            self._deliver_balls()
        self._collect_remaining_balls()


    def _collect_and_deliver_orange_ball(self):
        """
        Collects and delivers orange balls.
        """
        self.collect_orange_ball = True
        if len(self.orange_balls) == 0:
            return
        while len(self.orange_balls) > 0:
            self._collect_ball()
        self._deliver_balls()


    def _collect_remaining_balls(self):
        """
        Collects remaining white balls.
        """
        if self.white_balls is not None:
            while len(self.white_balls) > 0:
                self._collect_ball()
            self._deliver_balls()

    def _collect_ball(self):
        """
        Collects a single ball based on its position.
        """
        ret, frame = self.camera.read()
        warped_img = warp_perspective(frame, self.final_points, DST_SIZE)
        robot_pos, robot_direction = safe_detect_robot(self.camera, self.final_points, DST_SIZE, self.white, self.white)

        ret, frame = self.camera.read()
        warped_img = warp_perspective(frame, self.final_points, DST_SIZE)
        self.white_balls, self.orange_balls = detect_balls_with_model(warped_img)

        center_x = DST_SIZE[1] / 2
        center_y = DST_SIZE[0] / 2

        def distance_from_center(ball):
            x, y, _ = ball
            return math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        # Filter out the white balls within the specified radius
        self.white_balls = [ball for ball in self.white_balls if distance_from_center(ball) > 200]

        if len(self.orange_balls) > 0:
            self.target_pos = self.orange_balls[0][:2]
            self.collect_orange_ball = True
        elif self.collect_orange_ball:
            self.collect_orange_ball = False
            return
        elif self.white_balls is None or len(self.white_balls) == 0:
            return
        else:
            self.target_pos = find_nearest_ball(robot_pos, self.white_balls)

        if ball_is_in_corner(self.target_pos):
            self._collect_ball_in_corner(self.target_pos)

        elif ball_is_on_wall(self.target_pos, self.navmesh):
            self._collect_ball_on_wall(self.target_pos)

        else:
            self._is_in_dead_zone(self.navmesh, robot_pos, robot_direction)
            robot_pos, robot_direction = safe_detect_robot(
                self.camera, self.final_points, DST_SIZE, self.direction_color,
                self.pivot_color
            )
            path = find_path(self.navmesh, robot_pos, self.target_pos)
            if path is not None:
                self._navigate_to_target(path)
            else:
                pretty_print_navmesh(self.navmesh, path, robot_pos)
                return

    def _calc_robot_front(self, robot_direction, robot_pos):
        """
        Calculates the position in front of the robot.

        Parameters
        ----------
        robot_direction : tuple
            The current direction vector of the robot.
        robot_pos : tuple
            The current position of the robot.

        Returns
        -------
        tuple
            The position in front of the robot.
        """
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

    def _collect_ball_in_corner(self, ball_pos):
        """
        Collects a ball located in a corner.

        Parameters
        ----------
        ball_pos : tuple
            The position of the ball.
        """
        robot_pos, robot_direction = safe_detect_robot(
            self.camera, self.final_points, DST_SIZE, self.direction_color,
            self.pivot_color
        )
        result = check_corners(ball_pos, threshold=100)
        self.target_pos = get_pivot(result)
        path = find_path(self.navmesh, robot_pos, self.target_pos)
        self._navigate_to_target(path)
        angle = rotate_vector_to_point(robot_pos, robot_direction, ball_pos)

        tolerance = 10
        if angle < -tolerance or angle > tolerance:
            self._course_correction(angle, ball_pos, tol=tolerance)

        front_x, front_y = self._calc_robot_front(robot_direction, robot_pos)

        # Drive forward towards ball until front of robot enters buffer
        while not cell_is_in_border_zone((front_x, front_y), self.navmesh):
            self.client.send_command("start_drive 10")
            if angle < -tolerance or angle > tolerance:
                self._course_correction(angle, ball_pos, tol=tolerance)

            robot_pos, robot_direction = safe_detect_robot(
                self.camera, self.final_points, DST_SIZE, self.direction_color,
                self.pivot_color
            )
            front_x, front_y = self._calc_robot_front(robot_direction, robot_pos)

        self.client.send_command("stop")
        self.client.send_command("start_collect")
        self.client.send_command("move 10")
        if angle < -tolerance or angle > tolerance:
            self._course_correction(angle, ball_pos, tol=tolerance)
        self.client.send_command("move 9")
        self.client.send_command("move -20")
        self.client.send_command("stop_collect")
        self.client.send_command("stop")

    def _collect_ball_on_wall(self, ball_pos):
        """
        Collects a ball located on a wall.

        Parameters
        ----------
        ball_pos : tuple
            The position of the ball.
        """
        pivot_x, pivot_y = ball_pos

        adjustment = 200
        if pivot_x > 1800-adjustment:
            pivot_x = 1800-adjustment
        elif pivot_x < adjustment:
            pivot_x = adjustment
        if pivot_y > 1200-adjustment:
            pivot_y = 1200-adjustment
        elif pivot_y < adjustment:
            pivot_y = adjustment

        robot_pos, robot_direction = safe_detect_robot(
            self.camera, self.final_points, DST_SIZE, self.direction_color,
            self.pivot_color
        )
        path = find_path(self.navmesh, robot_pos, (pivot_x, pivot_y))
        self._navigate_to_target(path)

        angle = rotate_vector_to_point(robot_pos, robot_direction, ball_pos)

        tolerance = 10
        if angle < -tolerance or angle > tolerance:
            self._course_correction(angle, ball_pos, tol=tolerance)

        self.client.send_command("move 5")
        self.client.send_command("start_collect")
        self.client.send_command("move -5")
        self.client.send_command("stop_collect")

    def _deliver_balls(self):
        """
        Delivers collected balls to the goal.
        """
        log_path("Start deliver")
        ret, frame = self.camera.read()
        warped_img = warp_perspective(frame, self.final_points, DST_SIZE)

        robot_pos, robot_direction = detect_robot(warped_img, self.direction_color, self.pivot_color)
        while robot_pos is None or robot_direction is None:
            robot_pos, robot_direction = detect_robot(warped_img, self.direction_color, self.pivot_color)

        goal_A_pivot_point = (150, 600)

        while not are_points_close(robot_pos, goal_A_pivot_point, tolerance=50):
            robot_pos, robot_direction = safe_detect_robot(
                self.camera, self.final_points, DST_SIZE, self.direction_color,
                self.pivot_color
            )
            path = find_path(self.navmesh, robot_pos, goal_A_pivot_point)

            self.client.send_command("stop_collect")
            self._navigate_to_target(path)

        if not are_points_close(robot_pos, goal_A_pivot_point, tolerance=20):
            self._navigate_to_target([goal_A_pivot_point])

        angle = rotate_vector_to_point(robot_pos, robot_direction, (-100, 600))

        if angle < -1 or angle > 1:
            self._course_correction(angle, (-100, 600), 1)

        self.client.send_command("deliver")
        time.sleep(5)
        self.client.send_command("stop_collect")

    def _navigate_to_target(self, path):
        """
        Navigates the robot to the target position following the given path.

        Parameters
        ----------
        path : list
            The path to follow. List of coordinates [(x, y)]
        """
        if path is None:
            log_path("Can't navigate, no path.")
            return

        path_is_invalid = False
        for (x, y) in path:
            while True:
                robot_pos = None
                robot_direction = None
                while robot_pos is None or robot_direction is None:
                    ret, frame = self.camera.read()
                    gen_warped_image = warp_perspective(frame, self.final_points, DST_SIZE)
                    robot_pos, robot_direction = detect_robot(gen_warped_image, self.direction_color,
                                                              self.pivot_color)

                if robot_pos is None or robot_direction is None:
                    continue
                #Last minute removal of broken code
                # if self._is_in_dead_zone(self.navmesh, robot_pos, robot_direction) and self.tempdeadbool:
                #     path_is_invalid =True
                #     break
                if are_points_close(robot_pos, (x, y), tolerance=40):
                    self.client.send_command("stop")
                    self.robot_is_moving = False
                    self.at_target = True
                    self.tempdeadbool = True
                    break

                angle = rotate_vector_to_point(robot_pos, robot_direction, (x, y))

                tolerance = 10
                if angle < -tolerance or angle > tolerance:
                    self._course_correction(angle, (x, y), tol=tolerance)

                if not self.robot_is_moving and not self.robot_is_turning:
                    self.client.send_command("start_drive 10")
                    self.robot_is_moving = True

                # Check position and direction after starting to drive
                ret, frame = self.camera.read()
                gen_warped_image = warp_perspective(frame, self.final_points, DST_SIZE)
                robot_pos, robot_direction = detect_robot(gen_warped_image, self.direction_color, self.pivot_color)

                if self.robot_is_moving:
                    if are_points_close(robot_pos, (x, y), 300):
                        self.client.send_command("start_drive 10")
                    else:
                        self.client.send_command("start_drive 10")

                    if are_points_close(robot_pos, self.target_pos, 300):
                        self.client.send_command("start_collect")
                    else:
                        self.client.send_command("stop_collect")
            if path_is_invalid:
                log_path("path invalid, breaking")
                break

    def _course_correction(self, angle, target, tol=10.5):
        """
        Corrects the robot's course to align with the target.

        Parameters
        ----------
        angle : float
            The angle by which the robot needs to turn.
        target : tuple
            The target position.
        tol : float, optional
            The tolerance for course correction, default is 10.5.
        """
        while angle < -tol or angle > tol:
            ret, frame = self.camera.read()
            gen_warped_image = warp_perspective(frame, self.final_points, DST_SIZE)

            robot_pos = None
            robot_direction = None
            while robot_pos is None or robot_direction is None:
                ret, frame = self.camera.read()
                gen_warped_image = warp_perspective(frame, self.final_points, DST_SIZE)
                robot_pos, robot_direction = detect_robot(gen_warped_image, self.direction_color, self.pivot_color)

            if robot_pos is None or robot_direction is None:
                continue
            angle = rotate_vector_to_point(robot_pos, robot_direction, target)

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

    # BUG: Robot gets stuck in here and its just bad
    def _is_in_dead_zone(self, navmesh, robot_pos, robot_direction):
        """
        Checks if the robot is in a dead zone and navigates out if necessary.

        Parameters
        ----------
        navmesh : numpy.ndarray
            The navigation mesh.
        robot_pos : tuple
            The current position of the robot.
        robot_direction : tuple
            The current direction of the robot.

        Returns
        -------
        bool
            True if the robot is in a dead zone, False otherwise.
        """
        front_x, front_y = self._calc_robot_front(robot_direction, robot_pos)
        if cell_is_in_border_zone((front_x, front_y), navmesh):
            self._escape_border(robot_pos, robot_direction)
            return True
        elif cell_is_in_cross_zone((front_x, front_y), navmesh):
            self.tempdeadbool = False
            self.client.send_command("stop")
            cellCoord = coordinate_to_cell(front_x, front_y, GRID_SIZE)

            robot_pos, robot_direction = safe_detect_robot(
                    self.camera, self.final_points, DST_SIZE, self.direction_color,
                    self.pivot_color)

            temp = 500

            distance = math.sqrt((robot_pos[0] - 900-temp) ** 2 + (robot_pos[1] - 600) ** 2)
            target = (900-temp, 600)
            if distance > math.sqrt((robot_pos[0] - 900) ** 2 + (robot_pos[1] - 600-temp) ** 2):
                distance = math.sqrt((robot_pos[0] - 900) ** 2 + (robot_pos[1] - 600-temp) ** 2)
                target = (900, 600-temp)
            if distance > math.sqrt((robot_pos[0] - 900+temp) ** 2 + (robot_pos[1] - 600) ** 2):
                distance = math.sqrt((robot_pos[0] - 900+temp) ** 2 + (robot_pos[1] - 600) ** 2)
                target = (900+temp, 600)
            if distance > math.sqrt((robot_pos[0] - 900) ** 2 + (robot_pos[1] - 600+temp) ** 2):
                distance = math.sqrt((robot_pos[0] - 900) ** 2 + (robot_pos[1] - 600+temp) ** 2)
                target = (900, 600+temp)

            self._navigate_to_target([target])
            return True
        return False

    def _escape_border(self, robot_pos, robot_direction):
        """
        Escapes from a border zone by moving towards the center.

        Parameters
        ----------
        robot_pos : tuple
            The current position of the robot.
        robot_direction : tuple
            The current direction of the robot.
        """
        angle = rotate_vector_to_point(robot_pos, robot_direction, (900, 600))
        tolerance = 20
        if angle < -tolerance or angle > tolerance:
            self._course_correction(angle, (900, 600), tol=tolerance)
        self.client.send_command("move 10")

    def _escape_cross(self, front_x, front_y):
        """
        Escapes from a cross zone by moving backwards.

        Parameters
        ----------
        front_x : int
            The x-coordinate of the front of the robot.
        front_y : int
            The y-coordinate of the front of the robot.
        """
        log_path("front is in cross buffer")
        self.client.send_command("move -15")

    def temp(self):
        ret, frame = self.camera.read()
        warped_img = warp_perspective(frame, self.final_points, DST_SIZE)
        robot_pos, robot_direction = detect_robot(warped_img, self.direction_color, self.pivot_color)
        return robot_pos, robot_direction

    def _collect_ball_from_obstacle(self):
        pass


def cell_is_in_border_zone(pos, navmesh):
    target_cell = coordinate_to_cell(pos[0], pos[1], GRID_SIZE)
    return navmesh[int(target_cell[1]), int(target_cell[0])] == 0


def cell_is_in_cross_zone(pos, navmesh):
    target_cell = coordinate_to_cell(pos[0], pos[1], GRID_SIZE)
    return navmesh[int(target_cell[1]), int(target_cell[0])] == 1


def ball_is_on_wall(ball_pos, navmesh):
    return cell_is_in_border_zone(ball_pos, navmesh)


def ball_is_in_obstacle(ball_pos, navmesh):
    return cell_is_in_cross_zone(ball_pos, navmesh)

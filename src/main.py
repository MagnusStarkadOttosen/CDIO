import cv2
import numpy as np

from src.client.field.coordinate_system import are_points_close
from src.client.field.field import Field
from src.client.field.robot import calc_vector_direction, calc_degrees_to_rotate
from src.client.pc_client import ClientPC
from src.client.vision.camera import capture_image
from src.client.vision.filters import filter_image_white
from src.client.vision.pathfinder import find_nearest_ball
from src.client.vision.shape_detection import detect_balls, detect_robot

WHITE_BALL_COUNT = 10
ROBOT_CAPACITY = 6
TOLERANCE = 1
class Main:
        def __init__(self):
                self.client = ClientPC()
                self.balls = None

        def main_loop(self):
                # pretend ur working with a video that has one single frame
                # image_name = "gen_warped2_newCourse_bigDots.jpg"
                # temp_frame = cv2.imread('images/' + image_name)


                while len(self.balls) > WHITE_BALL_COUNT - ROBOT_CAPACITY - 1:
                        self._collect_white_balls()

                self._collect_orange_ball()
                self._deliver_balls_loop()

                while len(self.balls) > 0:
                        self._collect_white_balls()
                self._deliver_balls_loop()

        def _collect_white_balls(self):
                capture_image("test.jpg")
                image = cv2.imread("images/capturedImage/test.jpg")
                robot_pos, robot_direction = detect_robot(image)
                self.balls = detect_balls(image)

                target_pos = find_nearest_ball(robot_pos, self.balls)
                target_direction = calc_vector_direction(robot_pos, target_pos)

                if are_points_close(robot_pos, target_pos):
                        self.client.send_command("stop")
                        return

                deg = calc_degrees_to_rotate(robot_direction, target_direction)

                # Check if angle need to change
                if deg < -TOLERANCE or deg > TOLERANCE:
                        self.client.send_command("turn " + deg)
                        self.client.send_command("drive")

        def _collect_orange_ball(self):
                print("hei girl hei girl hei girl")

        def _deliver_balls_loop(self):
        # get angle to turn from current robot direction
        # send command to drive until robot_pos = goal_pos

        def _run_get_white_balls_loop(self, filtered_image):  # probably needs to be video feed here
                self.field.balls = detect_balls(filtered_image)




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

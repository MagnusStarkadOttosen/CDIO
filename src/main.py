import cv2
import numpy as np

from src.client.field.field import Field
from src.client.pc_client import ClientPC
from src.client.vision.filters import filter_image_white
from src.client.vision.shape_detection import detect_balls

WHITE_BALL_COUNT = 10
ROBOT_CAPACITY = 6

class Main:
        def __init__(self):
                self.client = ClientPC()
                self.field = None

        def main_loop(self):
                # pretend ur working with a video that has one single frame
                image_name = "gen_warped2_newCourse_bigDots.jpg"
                temp_frame = cv2.imread('images/' + image_name)
                self.field = Field(temp_frame)

                while len(self.field.balls) > WHITE_BALL_COUNT - ROBOT_CAPACITY - 1:
                        self._collect_white_balls()
                self._collect_orange_ball()
                self._deliver_balls_loop()

                while len(self.field.balls) > 0:
                        self._collect_white_balls()
                self._deliver_balls_loop()


        def _collect_orange_ball(self):
                print("hei girl hei girl hei girl")


        def _collect_white_balls(self):
                # this is the thing from the sequence diagram

        def _deliver_balls_loop(self):
                # get angle to turn from current robot direction
                # send command to drive until robot_pos = goal_pos


        # get_image
        # modify_image
        # update_robot_position
        # plan_path
        # move_robot


        def _run_get_white_balls_loop(self, filtered_image):  # probably needs to be video feed here
                self.field.balls = detect_balls(filtered_image)


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

import time

import cv2
import unittest

from src.client.field.robot import calc_degrees_to_rotate, calc_vector_direction
from src.client.vision.shape_detection import detect_balls, detect_robot
from src.client.pc_client import ClientPC


class TestMainLoop(unittest.TestCase):
    def run_main_loop(self):
        # OBS REMEMBER TO START SERVER IN OTHER TERMINAL WINDOW
        client_pc = ClientPC()
        image_name = "robot_ball_90.jpeg"
        image = cv2.imread('images/' + image_name)

        robot_pos, robot_direction = detect_robot(image)
        balls = detect_balls(image)

        # Would call find_nearest_ball in normal loop
        target_ball_pos = (balls[0][0], balls[0][1])

        target_direction = calc_vector_direction(target_ball_pos,
                                                 robot_pos)
        degrees_to_rotate = calc_degrees_to_rotate(robot_direction,
                                                   target_direction)

        client_pc.send_command("start_collect")
        client_pc.send_command(f"turn {degrees_to_rotate}")
        client_pc.send_command(f"exit")


    def move(self):
        client_pc = ClientPC()

        client_pc.send_command("start_collect")
        #client_pc.send_command("turn 90")
        #client_pc.send_command("move 23")

        time.sleep(45)
        client_pc.send_command("stop_collect")
        client_pc.send_command(f"exit")


import numpy as np

from src.server.robot import Robot, drive, turn


class CommandProcessor:

    def __init__(self):
        self.robot = Robot()
        self.is_moving = False
        self.is_rotating = False
        self.target_position = None
        self.target_rotation = None

    def start(self, x, y):
        self.target_position = np.array([x, y], dtype=int)

    def update(self):
        if self.robot.position == self.target_position:
            self.is_moving = False

        if self.robot.pivot == self.target_rotation:
            self.is_rotating = False

    def process_command(self, command):
        command_list = command.split(" ")
        action = command_list[0].toLower()
        value = command_list[1].toFloat()

        if action == "move":
            drive(value)
            self.is_moving = True
        elif action == "rotate":
            turn(value)
            self.is_rotating = True

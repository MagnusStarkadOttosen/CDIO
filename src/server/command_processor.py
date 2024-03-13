import numpy as np

from src.server.robot import Robot, move, turn


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
        try:
            action = command_list[0].lower()
            if action == "exit":
                print("Client closing connection.")
                return

            value = float(command_list[1])

            if action == "move":
                move(value, self.robot.tank_drive)
                self.is_moving = True
            elif action == "rotate":
                turn(value)
                self.is_rotating = True
            else:
                print('Invalid command')
        except IndexError as e:
            print(e)

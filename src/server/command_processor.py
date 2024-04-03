import time

from src.server.robot import drive, turn

"""
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
"""


def process_command(command):
    response = 0
    command_list = command.split(" ")
    try:
        action = command_list[0].lower()

        value = float(command_list[1])

        if action == "move":
            drive(value)
            # self.is_moving = True
        elif action == "rotate":
            turn(value)
            # self.is_rotating = True
        else:
            print('Invalid command')  # perhaps remove this and handle command formatting errors client-side
    except IndexError as e:
        print("Command should be in the format 'command int':", e)

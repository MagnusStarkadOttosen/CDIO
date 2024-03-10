import numpy as np

from src.vision.shape_detection import Robot


class CommandProcessor:

    def __init__(self):
        self.robot = Robot()
        self.isMoving = False
        self.isRotating = False
        self.targetPosition = None
        self.targetRotation = None

    def start(self, x, y):
        self.targetPosition = np.array([x, y], dtype=int)

    def update(self, x, y):
        self.targetPosition = np.array([x, y], dtype=int)
        # something missing here
        if self.robot.position == self.targetPosition:
            self.isMoving = False

        if self.robot.pivot == self.targetRotation:
            self.isRotating = False

    def process_command(self, command):
        command_list = command.split(" ")
        action = command_list[0].toLower()

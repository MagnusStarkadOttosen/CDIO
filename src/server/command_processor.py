import time

from src.server.robot import Robot
from src.server.robot_stub import RobotStub
robot = RobotStub() #Robot()


def process_command(command):
    command_list = command.split(" ")
    try:
        action = command_list[0].lower()

        value = float(command_list[1])

        if action == "move":
            robot.drive(value)
        elif action == "rotate":
            robot.turn_by_x_degrees(value)
        else:
            print('Invalid command')  # perhaps remove this and handle command formatting errors client-side

    except IndexError as e:
        print("Command should be in the format 'command int':", e)

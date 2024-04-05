import time

from src.server.commands import Robot
from src.server.commands_stub import RobotStub

robot = RobotStub()  # Robot()
actions_functions = {
    "move": robot.drive,
    "turn": robot.turn_by_x_degrees,
    "start_collect": robot.run_collector_clockwise,
    "deliver": robot.run_collector_counterclockwise,
    "stop_collect": robot.stop_collector
}


def process_command(command):
    command_parsed = command.split(" ")
    try:
        action = command_parsed[0].lower()
        if action in actions_functions:
            if len(command_parsed) > 1:
                value = float(command_parsed[1])
                actions_functions[action](value)
            else:
                actions_functions[action]()
        else:
            print("Invalid command")
    except IndexError as e:
        print("Command should be in the format 'command int':", e)

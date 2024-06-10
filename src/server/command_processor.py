import time

from src.server.commands import Commands
from src.server.commands_stub import CommandsStub

commands = Commands()  # Robot()
actions_functions = {
    # "move": commands.drive,
    "turn": commands.turn_by_x_degrees,
    "start_collect": commands.run_collector_clockwise,
    "deliver": commands.run_collector_counterclockwise,
    "stop_collect": commands.stop_collector,
    "stop": commands.stop,
    "start_drive": commands.drive_inf,
    "turn_left": commands.turn_left
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

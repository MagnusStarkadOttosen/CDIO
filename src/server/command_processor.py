import time

from src.server.robot import Robot
from src.server.robot_stub import RobotStub

robot = RobotStub()  # Robot()


def process_command(command):
    command_list = command.split(" ")
    try:
        action = command_list[0].lower()
        if len(command_list) > 1:
            value = float(command_list[1])
            if action == "move":
                robot.drive(value)
            elif action == "turn":
                robot.turn_by_x_degrees(value)
            else:
                print("Invalid")
        else:
            if action == "start_collect":
                robot.run_collector_clockwise()
            elif action == "deliver":
                robot.run_collector_counterclockwise()
            elif action == "stop_collect":
                robot.stop_collector()
            else:
                print('Invalid command')  # perhaps remove this and handle command formatting errors client-side

    except IndexError as e:
        print("Command should be in the format 'command int':", e)

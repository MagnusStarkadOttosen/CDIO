
import math
from src.client.field.navigate_robot_to_target import *
from src.client.pc_client import ClientPC


target_point = (300, 600)
turn_angle = 75
corner_point = (0, 0)
client_pc = ClientPC()


def calculate_distance(corner_point, target_point):
    return math.sqrt((target_point[0] - corner_point[0]) ** 2 + (target_point[1] - corner_point[1]) ** 2)


def deliver_points(client_pc, target_point):
    dist=calculate_distance(corner_point, target_point)
    print("test1")
    navigate_robot_to_target(client_pc, target_point)
    print("test2")
    client_pc.send_command(f"turn {turn_angle}")
    print("I am in deliver point")
    client_pc.send_command("start_collect")
    navigate_robot_to_target(client_pc,corner_point)

    client_pc.send_command("start_drive")
    client_pc.send_command(f"drive_backwards {dist}")
    client_pc.send_command(f"turn {-turn_angle}")
    client_pc.send_command("stop")

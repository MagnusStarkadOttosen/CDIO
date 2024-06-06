from src.client.pc_client import ClientPC
from src.client.field.collect_from_corner import collect_from_corner, calculate_distance
import cv2
import unittest





# client_pc = ClientPC()

print("In test_corners")
corner_point = (0, 0)
target_point = (300, 600)
#calculate_distance(corner_point, target_point)
print("After calculate_distance")
collect_from_corner(client_pc, target_point)
# client_pc.send_command("move 20")
print("After deliver_points")

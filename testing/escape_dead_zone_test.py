import cv2

from src.CONSTANTS import GRID_SIZE
from src.client.hsvLoad import read_hsv_values
from src.client.pathfinding.GenerateNavMesh import coordinate_to_cell, GenerateNavMesh, escape_dead_zone

# Paths
input_folder_path = 'originalImages/'
output_folder_path = 'NavMeshImage/'
image_name = 'PreWarpedCourse.jpg'
input_image_path = input_folder_path + image_name
output_image_path = output_folder_path + 'NavMesh_' + image_name

# Load the image
image = cv2.imread(input_image_path)

red_hsv_values = read_hsv_values('hsv_presets_red.txt')

grid_size = GRID_SIZE

start = coordinate_to_cell(900, 600, grid_size)
goal = coordinate_to_cell(1600, 600, grid_size)

# start = (30, 20)
#
# goal = (30, 10)

print(f"Start cell: {start}")
print(f"Goal cell: {goal}")

navmesh = GenerateNavMesh(image, red_hsv_values)

x, y = escape_dead_zone(navmesh, start)

print(x)
print(y)


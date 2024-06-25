import cv2

from src.client.hsvLoad import read_hsv_values
from src.client.pathfinding.FindPath import find_path
from src.client.pathfinding.GenerateNavMesh import GenerateNavMesh

input_folder_path = 'originalImages/'
output_folder_path = 'NavMeshImage/'
image_name = 'PreWarpedCourse.jpg'
input_image_path = input_folder_path + image_name
output_image_path = output_folder_path + 'NavMesh_' + image_name

# Load the image
image = cv2.imread(input_image_path)

red_hsv_values = read_hsv_values('hsv_presets_red.txt')

navmesh = GenerateNavMesh(image, red_hsv_values)

# start = (900, 600)
# goal = (1600, 600)

# start = (1600, 600)
# goal = (900, 600)

start = (1750, 600)
goal = (900, 600)

path = find_path(navmesh, start, goal)

print(path)


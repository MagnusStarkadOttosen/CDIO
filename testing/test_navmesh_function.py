# Paths
import cv2
from src.client.pathfinding.GenerateNavMesh import GenerateNavMesh, astar, optimize_path


input_folder_path = 'originalImages/'
output_folder_path = 'NavMeshImage/'
image_name = 'PreWarpedCourse.jpg'
input_image_path = input_folder_path + image_name
output_image_path = output_folder_path + 'NavMesh_' + image_name

# Load the image
image = cv2.imread(input_image_path)


def read_hsv_values(filename):
    hsv_values = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split()
            hsv_values[key] = int(value)
    return hsv_values

red_hsv_values = read_hsv_values('hsv_presets_red.txt')

navmesh = GenerateNavMesh(image, red_hsv_values)

start = (10, 10)
goal = (50, 20)

path = astar(navmesh, start, goal)

optimized_path = optimize_path(navmesh, path)

print(optimized_path)
import cv2

from src.client.hsvLoad import read_hsv_values
from src.client.pathfinding.FindPath import pretty_print_navmesh
from src.client.pathfinding.GenerateNavMesh import astar, GenerateNavMesh, optimize_path
from testing.NavMeshGenTest import overlay_path_on_image, draw_start_goal_on_image, overlay_tried_cells_on_image


# Paths
input_folder_path = 'originalImages/'
output_folder_path = 'NavMeshImage/'
image_name = 'PreWarpedCourse.jpg'
input_image_path = input_folder_path + image_name
output_image_path = output_folder_path + 'NavMesh_' + image_name

# Load the image
image = cv2.imread(input_image_path)

red_hsv_values = read_hsv_values('hsv_presets_red.txt')
start = (10, 10)
goal = (50, 20)

print(f"Start cell: {start}")
print(f"Goal cell: {goal}")

navmesh = GenerateNavMesh(image, red_hsv_values)
path = astar(navmesh, start, goal)
print(path)

opti_path = optimize_path(navmesh, path)
print(opti_path)

pretty_print_navmesh(navmesh, path)

grid_size = 30
combined_image = overlay_path_on_image(image, opti_path, grid_size)
combined_image = draw_start_goal_on_image(combined_image, start, goal, grid_size)
cv2.imwrite('Navmesh with Optimized Path.jpg', combined_image)


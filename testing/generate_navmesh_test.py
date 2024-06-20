import cv2
import numpy as np

from src.client.hsvLoad import read_hsv_values
from src.client.pathfinding.FindPath import pretty_print_navmesh
from src.client.pathfinding.GenerateNavMesh import astar, GenerateNavMesh, optimize_path, coordinate_to_cell
from testing.NavMeshGenTest import overlay_path_on_image, draw_start_goal_on_image


# Paths
input_folder_path = 'originalImages/'
output_folder_path = 'NavMeshImage/'
image_name = 'PreWarpedCourse.jpg'
input_image_path = input_folder_path + image_name
output_image_path = output_folder_path + 'NavMesh_' + image_name

# Load the image
image = cv2.imread(input_image_path)

red_hsv_values = read_hsv_values('hsv_presets_red.txt')

grid_size = 30

start = coordinate_to_cell(350, 600, grid_size)
goal = coordinate_to_cell(1600, 600, grid_size)

# start = (30, 20)
#
# goal = (30, 10)

print(f"Start cell: {start}")
print(f"Goal cell: {goal}")

navmesh = GenerateNavMesh(image, red_hsv_values)
path = astar(navmesh, start, goal)
print(path)

opti_path = optimize_path(navmesh, path)
print(opti_path)

pretty_print_navmesh(navmesh, path)

combined_image = overlay_path_on_image(image, opti_path, grid_size)
combined_image = draw_start_goal_on_image(combined_image, start, goal, grid_size)
cv2.imwrite('Navmesh with Optimized Path.jpg', combined_image)

# Create an image to visualize the navmesh
navmesh_img = np.zeros_like(image)
print("Created an image to visualize the navmesh")
# Draw rectangles on the navmesh image
for y in range(navmesh.shape[0]):
    for x in range(navmesh.shape[1]):
        if navmesh[y, x] == 2:
            cv2.rectangle(navmesh_img, (x * grid_size, y * grid_size),
                          ((x + 1) * grid_size, (y + 1) * grid_size), (0, 255, 0), -1)
print(" Drew rectangles on the navmesh image")
# Overlay the navmesh on the original image
overlay = cv2.addWeighted(combined_image, 0.5, navmesh_img, 0.5, 0)

combined_overlay = draw_start_goal_on_image(overlay, start, goal, grid_size)
cv2.imwrite('Navmesh.jpg', combined_overlay)


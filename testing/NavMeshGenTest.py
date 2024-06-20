import heapq
import cv2
import numpy as np
#
#
#
# # Paths
# input_folder_path = 'originalImages/'
# output_folder_path = 'NavMeshImage/'
# image_name = 'PreWarpedCourse.jpg'
# input_image_path = input_folder_path + image_name
# output_image_path = output_folder_path + 'NavMesh_' + image_name
#
# # Load the image
# image = cv2.imread(input_image_path)
#
#
# def read_hsv_values(filename):
#     hsv_values = {}
#     with open(filename, 'r') as file:
#         for line in file:
#             key, value = line.strip().split()
#             hsv_values[key] = int(value)
#     return hsv_values
#
# def inverted_filter_mask(image, hsv_values):
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#
#     lower_bound = np.array([hsv_values['LowerH'], hsv_values['LowerS'], hsv_values['LowerV']])
#     upper_bound = np.array([hsv_values['UpperH'], hsv_values['UpperS'], hsv_values['UpperV']])
#
#     mask = cv2.inRange(hsv, lower_bound, upper_bound)
#     inverted_mask = cv2.bitwise_not(mask)
#
#     return mask, inverted_mask
#
#
#
#
# # # def generate_navmesh(image):
#
# red_hsv_values = read_hsv_values('hsv_presets_red.txt')
# print("read hsv valuees")
# mask, inverted_red_mask = inverted_filter_mask(image, red_hsv_values)
# print("created mask")
# # Set the edge pixels to white
# edge_size = 20
# inverted_red_mask[:edge_size, :] = 255
# inverted_red_mask[-edge_size:, :] = 255
# inverted_red_mask[:, :edge_size] = 255
# inverted_red_mask[:, -edge_size:] = 255
# print(" Set the edge pixels to white")
# # Convert image to grayscale
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# height, width = gray.shape
# print("converted to gray")
# # Define the grid size for the navmesh
# grid_size = 30
# buffer_size = 100
#
# # Create an empty navmesh grid
# navmesh = np.zeros((height // grid_size, width // grid_size), dtype=np.uint8)
# print("Create an empty navmesh grid")
# # Create a buffer around the black areas
# # kernel = np.ones((buffer_size, buffer_size), np.uint8)
# kernel = np.ones((buffer_size, buffer_size), np.uint8)
# buffered_mask = cv2.erode(inverted_red_mask, kernel, iterations=2)
# print("buffered mask")
# cv2.imwrite('Mask.jpg', inverted_red_mask)
# cv2.imwrite('BMask.jpg', buffered_mask)
# # cv2.imshow('Mask', inverted_red_mask)
# # cv2.imshow('BMask', buffered_mask)
# print("imshow")
# # Fill the navmesh grid based on the buffered_mask
# for y in range(0, height, grid_size):
#     for x in range(0, width, grid_size):
#         # Skip cells near the edges of the image to create a buffer
#         if y < buffer_size or y + grid_size > height - buffer_size or x < buffer_size or x + grid_size > width - buffer_size:
#             continue
#         cell = buffered_mask[y:y + grid_size, x:x + grid_size]
#         # Calculate the percentage of the cell that is white
#         white_pixels = np.sum(cell == 255)
#         total_pixels = cell.size
#         if white_pixels / total_pixels >= 0.75:
#             navmesh[y // grid_size, x // grid_size] = 2
#         else:
#             navmesh[y // grid_size, x // grid_size] = 1
# print("Filled the navmesh grid based on the buffered_mask")
# # Create an image to visualize the navmesh
# navmesh_img = np.zeros_like(image)
# print("Created an image to visualize the navmesh")
# # Draw rectangles on the navmesh image
# for y in range(navmesh.shape[0]):
#     for x in range(navmesh.shape[1]):
#         if navmesh[y, x] == 2:
#             cv2.rectangle(navmesh_img, (x * grid_size, y * grid_size),
#                           ((x + 1) * grid_size, (y + 1) * grid_size), (0, 255, 0), -1)
# print(" Drew rectangles on the navmesh image")
# # Overlay the navmesh on the original image
# overlay = cv2.addWeighted(image, 0.5, navmesh_img, 0.5, 0)
# print(" Overlayed the navmesh on the original image")
# # Display the images
# # cv2.imshow('Original Image', image)
# # cv2.imshow('Navmesh', overlay)
#
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
# np.set_printoptions(threshold=np.inf)
# inverted_navmesh = np.logical_not(navmesh).astype(np.uint8)
# # print(inverted_navmesh)
# print("")
#
#
# def heuristic(a, b):
#     return abs(a[0] - b[0]) + abs(a[1] - b[1])
#
# def astar(navmesh, start, goal):
#     # Priority queue to store (cost, current_node)
#     open_set = []
#     heapq.heappush(open_set, (0, start))
#
#     # Dictionaries to store the cost from start to each node and the path
#     g_costs = {start: 0}
#     came_from = {start: None}
#
#     tried_cells = set()
#
#     while open_set:
#         _, current = heapq.heappop(open_set)
#         tried_cells.add(current)
#
#         if current == goal:
#             # Reconstruct the path
#             path = []
#             while current is not None:
#                 path.append(current)
#                 current = came_from[current]
#             path.reverse()
#             return path, tried_cells
#
#         # Get neighbors
#         neighbors = [
#             (current[0] + 1, current[1]),
#             (current[0] - 1, current[1]),
#             (current[0], current[1] + 1),
#             (current[0], current[1] - 1),
#             (current[0] + 1, current[1] + 1),
#             (current[0] - 1, current[1] - 1),
#             (current[0] + 1, current[1] - 1),
#             (current[0] - 1, current[1] + 1)
#         ]
#         for neighbor in neighbors:
#             if 0 <= neighbor[1] < navmesh.shape[0] and 0 <= neighbor[0] < navmesh.shape[1]:
#                 if navmesh[neighbor[1], neighbor[0]] == 2:  # Check if neighbor is walkable
#                     tentative_g_cost = g_costs[current] + 1
#                     if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
#                         g_costs[neighbor] = tentative_g_cost
#                         f_cost = tentative_g_cost + heuristic(neighbor, goal)
#                         heapq.heappush(open_set, (f_cost, neighbor))
#                         came_from[neighbor] = current
#         print(f"Considering neighbor: {neighbor} - Walkable: {navmesh[neighbor[1], neighbor[0]] if 0 <= neighbor[1] < navmesh.shape[0] and 0 <= neighbor[0] < navmesh.shape[1] else 'Out of bounds'}")
#
#     return None, tried_cells  # Path not found
#
# def pretty_print_navmesh(navmesh, path):
#     navmesh_copy = navmesh.copy()
#     for (x, y) in path:
#         navmesh_copy[y, x] = 3  # Mark the path with '3'
#
#     for row in navmesh_copy:
#         print(' '.join(str(cell) for cell in row))
#
# # Converts the coordinates from the image to the cell
# def coordinate_to_cell(x, y, grid_size):
#     cell_x = x // grid_size
#     cell_y = y // grid_size
#     return cell_x, cell_y
#
# # Converts the list of cells from a star to a list of coordinates
# def cells_to_coordinates(cells, grid_size):
#     coordinates = []
#     for cell_x, cell_y in cells:
#         top_left = (cell_x * grid_size, cell_y * grid_size)
#         bottom_right = ((cell_x + 1) * grid_size, (cell_y + 1) * grid_size)
#         coordinates.append((top_left, bottom_right))
#     return coordinates
#
def cell_to_image_coordinates(cell_x, cell_y, grid_size):
    top_left = (cell_x * grid_size, cell_y * grid_size)
    bottom_right = ((cell_x + 1) * grid_size, (cell_y + 1) * grid_size)
    return top_left, bottom_right
#
def overlay_path_on_image(image, path, grid_size):
    overlay = image.copy()
    for i in range(len(path) - 1):
        start_cell = path[i]
        end_cell = path[i + 1]
        start_coord = (start_cell[0] * grid_size + grid_size // 2, start_cell[1] * grid_size + grid_size // 2)
        end_coord = (end_cell[0] * grid_size + grid_size // 2, end_cell[1] * grid_size + grid_size // 2)
        cv2.arrowedLine(overlay, start_coord, end_coord, (255, 0, 0), 2, tipLength=0.3)
    combined_image = cv2.addWeighted(image, 0.7, overlay, 0.3, 0)
    return combined_image
#
def overlay_tried_cells_on_image(image, tried_cells, grid_size):
    overlay = image.copy()
    for (cell_x, cell_y) in tried_cells:
        top_left, bottom_right = cell_to_image_coordinates(cell_x, cell_y, grid_size)
        cv2.rectangle(overlay, top_left, bottom_right, (0, 255, 255), -1)  # Yellow color for tried cells
    combined_image = cv2.addWeighted(image, 0.7, overlay, 0.3, 0)
    return combined_image
#
def draw_start_goal_on_image(image, start, goal, grid_size):
    overlay = image.copy()
    start_top_left, start_bottom_right = cell_to_image_coordinates(start[0], start[1], grid_size)
    goal_top_left, goal_bottom_right = cell_to_image_coordinates(goal[0], goal[1], grid_size)

    cv2.rectangle(overlay, start_top_left, start_bottom_right, (0, 255, 255), -1)  # Yellow for start
    cv2.rectangle(overlay, goal_top_left, goal_bottom_right, (0, 0, 255), -1)     # Red for goal

    combined_image = cv2.addWeighted(image, 0.7, overlay, 0.3, 0)
    return combined_image
#
# def optimize_path(navmesh, path):
#     if not path:
#         return []
#
#     def is_straight_line(p1, p2, p3):
#         return (p1[0] - p2[0]) * (p2[1] - p3[1]) == (p1[1] - p2[1]) * (p2[0] - p3[0])
#
#     optimized_path = [path[0]]
#     for i in range(1, len(path) - 1):
#         if not is_straight_line(path[i - 1], path[i], path[i + 1]):
#             optimized_path.append(path[i])
#     optimized_path.append(path[-1])
#
#     return optimized_path
#
# def is_walkable(navmesh, start, end):
#     x0, y0 = start
#     x1, y1 = end
#     dx = abs(x1 - x0)
#     dy = abs(y1 - y0)
#     sx = 1 if x0 < x1 else -1
#     sy = 1 if y0 < y1 else -1
#     err = dx - dy
#     while True:
#         if navmesh[y0, x0] == 0 or navmesh[y0, x0] == 1:
#             return False
#         if (x0, y0) == (x1, y1):
#             break
#         e2 = err * 2
#         if e2 > -dy:
#             err -= dy
#             x0 += sx
#         if e2 < dx:
#             err += dx
#             y0 += sy
#     return True
#
# def smooth_path(navmesh, path):
#     if not path:
#         return path
#
#     smoothed_path = [path[0]]
#     i = 0
#
#     while i < len(path) - 1:
#         for j in range(len(path) - 1, i, -1):
#             if is_walkable(navmesh, path[i], path[j]):
#                 smoothed_path.append(path[j])
#                 i = j
#                 break
#         i += 1
#
#     return smoothed_path
#
#
# start = (10, 10)
# goal = (50, 20)
#
# # Check if start and goal are walkable
# if navmesh[start[1], start[0]] == 0 or navmesh[goal[1], goal[0]] == 0:
#     print(f"Start or goal is not in a walkable area. Start walkable: {navmesh[start[1], start[0]]}, Goal walkable: {navmesh[goal[1], goal[0]]}")
# else:
#     print(f"Start cell: {start}")
#     print(f"Goal cell: {goal}")
#
#     path, tried_cells = astar(navmesh, start, goal)
#
#     if path:
#         print("Path found:", path)
#         # pretty_print_navmesh(navmesh, path)
#
#         # optimize_path = path
#
#         # optimized_path = optimize_path(navmesh, path)
#         # print("Optimized Path:", optimized_path)
#
#         optimized_path = smooth_path(navmesh, path)
#         print("Optimized Path:", optimized_path)
#
#         combined_image = overlay_path_on_image(image, optimized_path, grid_size)
#         combined_image = draw_start_goal_on_image(combined_image, start, goal, grid_size)
#         combined_image = overlay_tried_cells_on_image(combined_image, tried_cells, grid_size)
#         cv2.imwrite('Navmesh with Optimized Path.jpg', combined_image)
#         start = (20, 30)
#         goal = (20, 33)
#         combined_overlay = draw_start_goal_on_image(image, start, goal, grid_size)
#         cv2.imwrite('Navmesh.jpg', combined_overlay)
#         # cv2.imshow('Navmesh with Optimized Path', combined_image)
#         # cv2.waitKey(0)
#         # cv2.destroyAllWindows()
#     else:
#         print("No path found.")
#         pretty_print_navmesh(navmesh, [])
#         combined_image = draw_start_goal_on_image(image, start, goal, grid_size)
#         combined_image = overlay_tried_cells_on_image(combined_image, tried_cells, grid_size)
#         cv2.imwrite('Navmesh with Path.jpg', combined_image)
#         # cv2.imshow('Navmesh with Path', combined_image)
#         # cv2.waitKey(0)
#         # cv2.destroyAllWindows()
#
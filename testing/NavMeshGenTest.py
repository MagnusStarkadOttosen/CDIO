import cv2
import numpy as np
from scipy.spatial import Delaunay
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
import matplotlib.pyplot as plt

from src.client.search_targetpoint.a_star_search import find_path

# Paths
input_folder_path = 'originalImages/'
output_folder_path = 'NavMeshImage/'
image_name = 'PreWarpedCourse.jpg'
input_image_path = input_folder_path + image_name
output_image_path = output_folder_path + 'NavMesh_' + image_name

# Load the image
image = cv2.imread(input_image_path)

# # Convert to grayscale
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Threshold the image to create a binary image
# _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

# # Find contours
# contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # Create vertices and polygons for the navmesh
# vertices = []
# for contour in contours:
#     for point in contour:
#         x, y = point[0]
#         vertices.append((x, y))

# # Perform Delaunay triangulation
# points = np.array(vertices)
# delaunay = Delaunay(points)
# triangles = points[delaunay.simplices]

# # Filter out small contours that cannot form valid polygons
# filtered_contours = [contour for contour in contours if len(contour) >= 3]

# # Create obstacle polygons
# obstacle_polygons = [Polygon(contour[:, 0, :]) for contour in filtered_contours]
# combined_obstacles = unary_union(obstacle_polygons)

# # Function to check if a triangle intersects with any obstacle
# def is_triangle_valid(triangle, obstacles):
#     poly = Polygon(triangle)
#     return not poly.intersects(obstacles)

# # Filter valid triangles
# valid_triangles = [tri for tri in triangles if is_triangle_valid(tri, combined_obstacles)]

# # Create an output image to draw the navmesh
# output_image = image.copy()

# # Draw the valid triangles
# for tri in valid_triangles:
#     pts = np.array(tri, np.int32)
#     pts = pts.reshape((-1, 1, 2))
#     cv2.polylines(output_image, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

# # Save the resulting image
# cv2.imwrite(output_image_path, output_image)

# # Display the result
# cv2.imshow('Navmesh', output_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


def read_hsv_values(filename):
    hsv_values = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split()
            hsv_values[key] = int(value)
    return hsv_values

def inverted_filter_mask(image, hsv_values):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_bound = np.array([hsv_values['LowerH'], hsv_values['LowerS'], hsv_values['LowerV']])
    upper_bound = np.array([hsv_values['UpperH'], hsv_values['UpperS'], hsv_values['UpperV']])

    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    inverted_mask = cv2.bitwise_not(mask)
    
    return mask, inverted_mask 










# # def generate_navmesh(image):

red_hsv_values = read_hsv_values('hsv_presets_red.txt')
mask, inverted_red_mask = inverted_filter_mask(image, red_hsv_values)


# # Downsample the image
# downsample_factor = 100
# small_image = inverted_red_mask[::downsample_factor, ::downsample_factor]

# # Dilate the black areas
# kernel_size = 3  # Adjust this to change the distance from black areas
# kernel = np.ones((kernel_size, kernel_size), np.uint8)
# dilated_image = cv2.dilate(1 - small_image, kernel)

# # Invert the image to get the navmesh areas
# navmesh = 1 - dilated_image

# # Ensure navmesh stays away from edges
# edge_padding = 1  # Adjust based on how far from the edges you want to stay
# navmesh[:edge_padding, :] = 0
# navmesh[-edge_padding:, :] = 0
# navmesh[:, :edge_padding] = 0
# navmesh[:, -edge_padding:] = 0

# # Plot the results
# plt.figure(figsize=(12, 8))
# plt.subplot(1, 2, 1)
# plt.title("Original Image")
# plt.imshow(inverted_red_mask, cmap='gray')

# plt.subplot(1, 2, 2)
# plt.title("Navmesh")
# plt.imshow(navmesh, cmap='gray')

# plt.show()


# # Find contours
# contours, _ = cv2.findContours(inverted_red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # Draw contours on the image to visualize the navmesh
# navmesh = image.copy()
# cv2.drawContours(navmesh, contours, -1, (0, 255, 0), 3)

# # Display the images
# cv2.imshow('Original Image', image)
# cv2.imshow('Mask', inverted_red_mask)
# # # cv2.imshow('Navmesh', navmesh)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()


# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# height, width = gray.shape

# # Create the navmesh grid
# grid_size = 30  # Change this value to adjust the granularity of the navmesh
# navmesh = np.zeros((height // grid_size, width // grid_size), dtype=np.uint8)

# for y in range(0, height, grid_size):
#         for x in range(0, width, grid_size):
#             cell = inverted_red_mask[y:y + grid_size, x:x + grid_size]
#             if np.any(cell == 255):  # If any part of the cell is walkable
#                 navmesh[y // grid_size, x // grid_size] = 1

# navmesh_img = np.zeros_like(image)
# grid_size = 30
# for y in range(navmesh.shape[0]):
#     for x in range(navmesh.shape[1]):
#         if navmesh[y, x] == 1:
#             cv2.rectangle(navmesh_img, (x * grid_size, y * grid_size), ((x + 1) * grid_size, (y + 1) * grid_size), (0, 255, 0), -1)

# # Overlay the navmesh on the original image
# overlay = cv2.addWeighted(image, 0.5, navmesh_img, 0.5, 0)

# # Display the images
# cv2.imshow('Original Image', image)
# # cv2.imshow('Walkable Area', inverted_filter_mask)
# cv2.imshow('Navmesh', overlay)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
    








# Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
height, width = gray.shape

# Define the grid size for the navmesh
grid_size = 30
buffer_size = 100

# Create an empty navmesh grid
navmesh = np.zeros((height // grid_size, width // grid_size), dtype=np.uint8)

# Create a buffer around the black areas
# kernel = np.ones((buffer_size, buffer_size), np.uint8)
kernel = np.ones((buffer_size, buffer_size), np.uint8)
buffered_mask = cv2.erode(inverted_red_mask, kernel, iterations=2)

cv2.imshow('Mask', inverted_red_mask)
cv2.imshow('BMask', buffered_mask)

# Fill the navmesh grid based on the buffered_mask
for y in range(0, height, grid_size):
    for x in range(0, width, grid_size):
        # Skip cells near the edges of the image to create a buffer
        if y < buffer_size or y + grid_size > height - buffer_size or x < buffer_size or x + grid_size > width - buffer_size:
            continue
        cell = buffered_mask[y:y + grid_size, x:x + grid_size]
        # Calculate the percentage of the cell that is white
        white_pixels = np.sum(cell == 255)
        total_pixels = cell.size
        if white_pixels / total_pixels >= 0.75:
            navmesh[y // grid_size, x // grid_size] = 1

# Create an image to visualize the navmesh
navmesh_img = np.zeros_like(image)

# Draw rectangles on the navmesh image
for y in range(navmesh.shape[0]):
    for x in range(navmesh.shape[1]):
        if navmesh[y, x] == 1:
            cv2.rectangle(navmesh_img, (x * grid_size, y * grid_size), 
                          ((x + 1) * grid_size, (y + 1) * grid_size), (0, 255, 0), -1)

# Overlay the navmesh on the original image
overlay = cv2.addWeighted(image, 0.5, navmesh_img, 0.5, 0)

# Display the images
cv2.imshow('Original Image', image)
cv2.imshow('Navmesh', overlay)
cv2.waitKey(0)
cv2.destroyAllWindows()
np.set_printoptions(threshold=np.inf)
inverted_navmesh = np.logical_not(navmesh).astype(np.uint8)
print(inverted_navmesh)

src = [10, 10]
dest = [30, 30]

# Run the A* search algorithm
asdf = find_path(inverted_navmesh, src, dest)
if asdf:
    for(i, j) in asdf:
       inverted_navmesh[j][i] = 3
    for row in inverted_navmesh:
        print("".join(str(cell) for cell in row))
print(asdf)
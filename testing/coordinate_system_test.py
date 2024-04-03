
import cv2
import numpy as np

from src.vision.shape_detection import Shapes
from testing.visualization import draw_shapes
from src.vision.coordinate_system import *
from src.vision.filters import *
from sklearn.cluster import KMeans
from src.vision.shape_detection import Shapes
from testing.visualization import draw_shapes
from src.vision.buffer_zone import draw_center_and_lines

# Manually placed corners on original image
# corners = np.array([[417, 73], [1650, 66], [1689, 987], [403, 985]], dtype="float32") #Top left, top right, buttom right, buttom left
# corners = np.array([[393, 49], [1678, 42], [1723, 1005], [378, 1000]], dtype="float32")
corners = np.array([[455, 58], [1656, 65], [1650, 933], [444, 945]], dtype="float32")

# Real world dimensions in cm
real_world_size = (120, 180)  # height, width

# Desired output size (dimensions in pixels for the warped image)
dst_size = (1200, 1800)  # width, height



# Path from where images comes from and path where the processed images are stored
input_folder_path = 'images/'
output_folder_path = 'images/'

# Name of the image to be used
image_name = '9.jpg'
input_image_path = input_folder_path + image_name
image = cv2.imread(input_image_path)

# Initialize shape detection
shape_detector = Shapes(image)
shape_detector.detect_balls()
shape_detector.detect_red_walls()

if image is not None:
    # Warped perspective for manual placed points.
    warped_image = warp_perspective(image, corners, dst_size)
    warped_image_name = 'warped_' + image_name
    warped_image_path = output_folder_path + warped_image_name
    cv2.imwrite(warped_image_path, warped_image)

    # Add a grid to the warped image.
    grid_image = draw_grid(warped_image, real_world_size, grid_spacing_cm=10)
    grid_image_name = 'grid_' + image_name
    grid_image_path = output_folder_path + grid_image_name
    cv2.imwrite(grid_image_path, grid_image)

    # Filter to only show the red walls from the original image.
    red_image = detect_red(image)
    red_image_name = 'red_' + image_name
    red_image_path = output_folder_path + red_image_name
    cv2.imwrite(red_image_path, red_image)

    # Filter to sharpen the edges on the red image
    sharp_image = sharpen_image(red_image)
    sharp_image_name = 'sharp_' + image_name
    sharp_image_path = output_folder_path + sharp_image_name
    cv2.imwrite(sharp_image_path, sharp_image)

    clean_image = clean_image(red_image)
    edge_image, lines = find_lines(clean_image)

    arr = np.array(lines)

    print(arr.shape)
    arr = arr.reshape(-1, 4)
    print(arr.shape)

    lines = np.array(lines)
    lines = lines.reshape(-1, 4)
    intersection_points = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            slope1 = calculate_slope(lines[i])
            slope2 = calculate_slope(lines[j])
            if is_near_90_degrees(slope1, slope2):
                intersection = find_intersection(lines[i], lines[j])
                if intersection:
                    intersection_points.append(intersection)
                    print(f"Intersection point: {intersection}")
                    cv2.circle(clean_image, intersection, radius=5, color=(255, 0, 0), thickness=-1)

    clean_image_name = 'clean_' + image_name
    clean_image_path = output_folder_path + clean_image_name
    cv2.imwrite(clean_image_path, clean_image)

    height, width, _ = image.shape
    center_x, center_y = width // 2, height // 2

    quadrants = {1: [], 2: [], 3: [], 4: []}

    # Categorize points into quadrants
    for point in intersection_points:
        x, y = point
        if x > center_x and y < center_y:
            quadrants[1].append(point)  # Quadrant I
        elif x < center_x and y < center_y:
            quadrants[2].append(point)  # Quadrant II
        elif x < center_x and y > center_y:
            quadrants[3].append(point)  # Quadrant III
        elif x > center_x and y > center_y:
            quadrants[4].append(point)  # Quadrant IV

    # Find the closest point to the center in each quadrant
    closest_points = []
    for q in [2, 1, 4, 3]:
        if quadrants[q]:  # Check if the list is not empty
            closest_point = min(quadrants[q], key=lambda point: distance_between_points(point, (center_x, center_y)))
            closest_points.append(closest_point)

    new_image = image

    for point in closest_points:
        print(f"Closest point in Quadrant to center: {point}")
        cv2.circle(new_image, point, radius=5, color=(255, 0, 0), thickness=-1)

    new_image_name = 'new_' + image_name
    new_image_path = output_folder_path + new_image_name
    cv2.imwrite(new_image_path, new_image)

    edge_image_name = 'edge_' + image_name
    edge_image_path = output_folder_path + edge_image_name
    cv2.imwrite(edge_image_path, edge_image)

    print(corners)
    print(closest_points)

    final_points = np.array(closest_points, dtype="float32")
    print(final_points)

    print(find_corner_points(image))

    gen_warped_image = warp_perspective(image, final_points, dst_size)

    gen_warped_image_name = 'gen_warped_' + image_name
    gen_warped_image_path = output_folder_path + gen_warped_image_name
    cv2.imwrite(gen_warped_image_path, gen_warped_image)


    if shape_detector.circles is not None or shape_detector.lines is not None:
        draw_shapes(shape_detector.circles, shape_detector.lines, image)

    buffer_zone_image_name = 'buffer_zone_' + image_name
    buffer_zone_image_path = output_folder_path + buffer_zone_image_name
    buffer_zone_image_name=gen_warped_image.copy()
    draw_center_and_lines(buffer_zone_image_name)
    cv2.imwrite( buffer_zone_image_path, buffer_zone_image_name)
    print(f"Processed image done!")
else:
    print("Error: Image not found. Please check the input folder path and image name.")
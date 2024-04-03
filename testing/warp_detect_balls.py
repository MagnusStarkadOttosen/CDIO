import cv2
import numpy as np
from src.vision.shape_detection import Shapes
from src.vision.coordinate_system import warp_perspective
from testing.visualization import draw_shapes
from src.vision.buffer_zone import draw_center_and_lines

# Configuration parameters
corners = np.array([[377, 44], [1382, 50], [1377, 779], [368, 791]], dtype="float32")
real_world_size = (120, 180)  # height, width in cm
dst_size = (1200, 1800)  # width, height in pixels
input_folder_path = 'images/'
output_folder_path = 'images/'  # Make sure this directory exists
image_name = '.jpg'

# Construct the full input and output image paths
input_image_path = input_folder_path + image_name
output_image_path_base = output_folder_path + image_name.split('.')[0]  # Base path for output images

# Load the image
image = cv2.imread(input_image_path)
if image is None:
    print("Error: Image not found. Please check the input folder path and image name.")
    exit()

# Initialize shape detection
shape_detector = Shapes(image)
shape_detector.detect_balls()
shape_detector.detect_red_walls()

# Debugging: Draw detected shapes and corners on the original image for verification
#shape_detector.draw_corners_debug(image)
#shape_detector.draw_coordinate_system(image)
if shape_detector.circles is not None or shape_detector.lines is not None:
    draw_shapes(shape_detector.circles, shape_detector.lines, image)

# Warp the perspective of the image
warped_image = warp_perspective(image, corners, dst_size)

# Additional processing on the warped image
lines_image = warped_image.copy()
draw_center_and_lines(lines_image)  # Drawing center and lines on the warped image

# Save processed images
cv2.imwrite(output_image_path_base + '_original_debug.jpg', image)  # Original image with debug drawings
cv2.imwrite(output_image_path_base + '_warped.jpg', warped_image)  # Warped image
cv2.imwrite(output_image_path_base + '_lines.jpg', lines_image)  # Warped image with lines

print(f"Processed images have been saved to {output_folder_path}")

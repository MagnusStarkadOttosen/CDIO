import cv2
import numpy as np

# Define global variables for the points and drawing properties
POINT_A = (100, 100)
POINT_B = (1700, 100)
POINT_C = (1700, 1100)
POINT_D = (100, 1100)
SQUARE_POINTS = [POINT_A, POINT_B, POINT_C, POINT_D]

LINE_COLOR = (0, 255, 0)  # Green color in BGR
LINE_THICKNESS = 3

def draw_center_and_lines(img):
    """
    Draw a square and lines between global points on the image.

    Args:
    - img: The image where the square will be drawn.
    """
    # Draw the square
    # Draw the square
    num_points = len(SQUARE_POINTS)
    for i in range(num_points):
        start_point = SQUARE_POINTS[i]
        end_point = SQUARE_POINTS[(i + 1) % num_points]  # Wrap around to the first point
        cv2.line(img, start_point, end_point, LINE_COLOR, LINE_THICKNESS)

    # Draw the lines between all points
    # for i in range(num_points):
    #     for j in range(i + 1, num_points):
    #         cv2.line(img, SQUARE_POINTS[i], SQUARE_POINTS[j], LINE_COLOR, LINE_THICKNESS)

# Create a blank image
image_size = (1800, 1200, 3)
image = np.zeros(image_size, dtype=np.uint8)
# Draw the square and lines
draw_center_and_lines(image)


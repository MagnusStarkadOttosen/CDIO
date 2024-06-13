import numpy as np

buffer_points = [(100, 100), (1700, 100), (1700, 1100), (100, 1100)]
buffer_distance = 100

# Determine the top-left and bottom-right points of the rectangle
green_zone_top_left = (min(point[0] for point in buffer_points), min(point[1] for point in buffer_points))
green_zone_bottom_right = (max(point[0] for point in buffer_points), max(point[1] for point in buffer_points))


def is_within_buffer_zone(robot_position):
 # Check if the robot position is outside the rectangular buffer zone (green zone)
 if (robot_position[0] < green_zone_top_left[0] or
         robot_position[0] > green_zone_bottom_right[0] or
         robot_position[1] < green_zone_top_left[1] or
         robot_position[1] > green_zone_bottom_right[1]):
  print("Warning: Robot is outside the buffer zone!")
  return True
 else:
  print("Robot is inside the buffer zone")
 return False



#
# # Define global variables for the points and drawing properties
# POINT_A = (100, 100)
# POINT_B = (1700, 100)
# POINT_C = (1700, 1100)
# POINT_D = (100, 1100)
# SQUARE_POINTS = [POINT_A, POINT_B, POINT_C, POINT_D]
#
# LINE_COLOR = (0, 255, 0)  # Green color in BGR
# LINE_THICKNESS = 3
#
# def draw_center_and_lines(img):
#     """
#     Draw a square and lines between global points on the image.
#
#     Args:
#     - img: The image where the square will be drawn.
#     """
#     # Draw the square
#     # Draw the square
#     num_points = len(SQUARE_POINTS)
#     for i in range(num_points):
#         start_point = SQUARE_POINTS[i]
#         end_point = SQUARE_POINTS[(i + 1) % num_points]  # Wrap around to the first point
#         cv2.line(img, start_point, end_point, LINE_COLOR, LINE_THICKNESS)
#
#     # Draw the lines between all points
#     # for i in range(num_points):
#     #     for j in range(i + 1, num_points):
#     #         cv2.line(img, SQUARE_POINTS[i], SQUARE_POINTS[j], LINE_COLOR, LINE_THICKNESS)
#
# # Create a blank image
# image_size = (1800, 1200, 3)
# image = np.zeros(image_size, dtype=np.uint8)
# # Draw the square and lines
# draw_center_and_lines(image)
#

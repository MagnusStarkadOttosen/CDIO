import cv2
import numpy as np
import logging

from src.client.utilities import log_balls

logging.basicConfig(filename='safe_detect_balls.log', filemode='w',
                    format='%(asctime)s - %(message)s')

from src.client.field.robot import calc_vector_direction
from src.client.vision.filters import clean_the_image, convert_hsv, filter_for_yellow, filter_image, filter_image_green, \
    filter_image_red, temp_filter_for_red_wall
from src.client.field.coordinate_system import calculate_slope, find_corner_points_full, find_corners, find_lines, \
    is_near_90_degrees, warp_perspective
from src.client.vision.filters import apply_gray, apply_canny
from src.client.field.coordinate_system import find_intersection


def safe_detect_robot(camera, final_points, dst_size, direction_col, pivot_col):
    while True:
        ret, frame = camera.read()
        warped_img = warp_perspective(frame, final_points, dst_size)
        robot_pos, robot_direction = detect_robot(warped_img, direction_col,
                                                  pivot_col)
        if robot_pos is not None and robot_direction is not None:
            return robot_pos, robot_direction


def detect_robot(image, direction_color, pivot_color):
    direction_dot = detect_balls(filter_image(image, direction_color), min_radius=45, max_radius=50)
    if len(direction_dot) < 1: 
        print("No direction dot.")
        return None, None

    pivot_dot = detect_balls(filter_image(image, pivot_color), min_radius=60, max_radius=65)
    if len(pivot_dot) < 1: 
        print("No pivot dot.")
        return None, None
    robot_pos = (pivot_dot[0][0], pivot_dot[0][1])
    robot_direction = calc_vector_direction(direction_dot[0], robot_pos)

    return robot_pos, robot_direction


def detect_egg(image, min_radius=45, max_radius=55):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection
    edges = cv2.Canny(gray, 110, 200)

    # Detect circles
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT,
                               dp=1.75, minDist=60,
                               param1=30, param2=35,
                               minRadius=min_radius, maxRadius=max_radius)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
    else:
        print("No balls detected.")

    return circles


def safe_detect_balls(camera, final_points, dst_size, color):
    temp_len = 0
    circles = None

    for i in range(10):
        ret, frame = camera.read()
        warped_img = warp_perspective(frame, final_points, dst_size)
        temp_circles = detect_balls(filter_image(warped_img, color))
        if temp_circles is not None:
            log_balls(f"{i}: {len(temp_circles)}")
        if temp_circles is not None and len(temp_circles) > temp_len:
            temp_len = len(temp_circles)
            circles = temp_circles

    if circles is not None:
        return circles
    return []


def detect_balls(image, min_radius=15, max_radius=25):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Apply edge detection
    edges = cv2.Canny(blurred, 50, 150)

    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT,
                               dp=1.75, minDist=9,
                               param1=30, param2=35,
                               minRadius=min_radius, maxRadius=max_radius)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        return circles

    return []


def detect_obstacles(image):
    red_image = temp_filter_for_red_wall(image)
    clean_image = clean_the_image(red_image)
    edge_image, lines = find_lines(clean_image, resolution=5, doVerbose=True)
    intersections = []
    if lines is not None:
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                l1 = lines[i][0]
                l2 = lines[j][0]
                slope1 = calculate_slope(l1)
                slope2 = calculate_slope(l2)
                if is_near_90_degrees(slope1, slope2, tolerance=5, zero_tolerance=0.1):
                    inter = find_intersection(l1, l2)
                    if inter is not None and inter not in intersections:
                        intersections.append(inter)
                        print(f"Intersection found: {inter}")
                        cv2.circle(clean_image, inter, radius=5, color=(255, 0, 0), thickness=-1)
    grouped_points = group_close_points(intersections)
    midpoint = calculate_midpoints(grouped_points)

    output_folder_path = 'images/outputObstacle/'
    re_image_path = output_folder_path + "re_image.jpg"
    cv2.imwrite(re_image_path, clean_image)
    
    return intersections, midpoint


def group_close_points(points, distance_threshold=10):
    groups = []
    for point in points:
        added = False
        for group in groups:
            if np.linalg.norm(np.array(point) - np.array(group[0])) < distance_threshold:
                group.append(point)
                added = True
                break
        if not added:
            groups.append([point])
    return groups


# fine the midpoint of the groups
def calculate_midpoints(groups):
    midpoint = [0][0]
    for group in groups:
        x = 0
        y = 0
        for point in group:
            x += point[0]
            y += point[1]
        midpoint = (x // len(group), y // len(group))
    return midpoint

class Shapes:  # TODO opløs Shapes klasse
    def __init__(self, image):
        self.original_image = image
        self.image = None
        self.detect_red_walls()
        self.image = apply_gray(image)
        self.circles = None
        self.lines = None

    def detect_walls(self):
        canny = apply_canny(self.image)
        self.lines = \
            cv2.HoughLinesP(canny, 1, np.pi / 180, 50, None, 50, 10)

    def detect_red_walls(self):
        hsv = convert_hsv(self.original_image)
        lower_red1 = np.array([0, 70, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 70, 50])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        self.image = cv2.bitwise_and(self.original_image, self.original_image, mask=mask)

    def draw_coordinate_system(image):
        corners = find_corners(image)  # Assuming this returns the corners as (x, y) tuples
        if corners is not None and len(corners) >= 4:
            # Assuming top-left and bottom-right corners are what we need
            # This might need adjustment based on how corners are ordered
            top_left = tuple(corners[0].ravel())
            bottom_right = tuple(corners[2].ravel())

            # Determine the number of lines in the grid (you can adjust this)
            num_lines = 10

            # Draw horizontal lines
            for i in range(num_lines + 1):
                start_point = (top_left[0], top_left[1] + i * ((bottom_right[1] - top_left[1]) // num_lines))
                end_point = (bottom_right[0], top_left[1] + i * ((bottom_right[1] - top_left[1]) // num_lines))
                cv2.line(image, start_point, end_point, (255, 255, 0), 2)  # Using yellow for visibility

            # Draw vertical lines
            for i in range(num_lines + 1):
                start_point = (top_left[0] + i * ((bottom_right[0] - top_left[0]) // num_lines), top_left[1])
                end_point = (top_left[0] + i * ((bottom_right[0] - top_left[0]) // num_lines), bottom_right[1])
                cv2.line(image, start_point, end_point, (255, 255, 0), 2)  # Using yellow for visibility


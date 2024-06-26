import cv2
import numpy as np
import logging

from src.client.utilities import log_balls

logging.basicConfig(filename='safe_detect_balls.log', filemode='w',
                    format='%(asctime)s - %(message)s')

from src.client.field.robot import calc_vector_direction
from src.client.vision.filters import clean_the_image,  filter_image, \
    temp_filter_for_red_wall
from src.client.field.coordinate_system import calculate_slope, find_lines, \
    is_near_90_degrees, warp_perspective
from src.client.field.coordinate_system import find_intersection


def safe_detect_robot(camera, final_points, dst_size, direction_col, pivot_col):
    while True:
        print("from safe_detect_robot")
        ret, frame = camera.read()
        warped_img = warp_perspective(frame, final_points, dst_size)
        robot_pos, robot_direction = detect_robot(warped_img, direction_col,
                                                  pivot_col)
        print(f"from safe_detect_robot: {robot_pos}, {robot_direction}")
        if robot_pos is not None and robot_direction is not None:
            print("from if")
            return robot_pos, robot_direction


def detect_robot(image, direction_color, pivot_color):
    direction_dot = detect_balls(filter_image(image, direction_color), min_radius=45, max_radius=50)
    if len(direction_dot) < 1:  # TODO Proper error handling for green_dot
        print("No direction dot.")
        return None, None

    pivot_dot = detect_balls(filter_image(image, pivot_color), min_radius=60, max_radius=65)
    if len(pivot_dot) < 1:  # TODO Proper error handling for red_dot
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

    # Detect circles
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT,
                               dp=1.75, minDist=9,
                               param1=30, param2=35,
                               minRadius=min_radius, maxRadius=max_radius)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        # print("balls count: ", len(circles))
    else:
        print("No balls detected.")
        circles = np.array([])

    return circles

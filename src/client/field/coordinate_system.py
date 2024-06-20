import math
import cv2
import numpy as np

from src.client.vision.filters import *
from sklearn.cluster import KMeans


def find_corners(masked_image):
    corners = cv2.goodFeaturesToTrack(cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY), 4, 0.01, 10)
    corners = np.int0(corners)
    return corners


def map_to_coordinate_system(image, point, origin, scale):
    # Convert a point from image coordinates to your defined coordinate system
    x, y = point
    origin_x, origin_y = origin
    mapped_x = (x - origin_x) * scale
    mapped_y = (y - origin_y) * scale
    return mapped_x, mapped_y


def warp_perspective(image, src_points, dst_size):
    height, width = dst_size

    pts_dst = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype="float32")

    M = cv2.getPerspectiveTransform(src_points, pts_dst)

    warped_image = cv2.warpPerspective(image, M, (width, height))

    return warped_image


def get_transformed_center(image, src_points, dst_size):
    height, width = dst_size

    pts_dst = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype="float32")

    M = cv2.getPerspectiveTransform(src_points, pts_dst)

    original_center = np.array([[[image.shape[1] / 2, image.shape[0] / 2]]], dtype="float32")
    transformed_center = cv2.perspectiveTransform(original_center, M)
    transformed_center = transformed_center.reshape((2,))
    print(f"transformed_center = {transformed_center}")

    return transformed_center


def draw_grid(image, real_world_size, grid_spacing_cm):
    height, width = image.shape[:2]

    scale_x = width / real_world_size[1]
    scale_y = height / real_world_size[0]

    num_x_lines = int(real_world_size[1] / grid_spacing_cm)
    num_y_lines = int(real_world_size[0] / grid_spacing_cm)

    image_with_grid = image.copy()

    for i in range(num_x_lines + 1):
        x = int(i * grid_spacing_cm * scale_x)
        cv2.line(image_with_grid, (x, 0), (x, height), (255, 255, 0), 2)

    for i in range(num_y_lines + 1):
        y = int(i * grid_spacing_cm * scale_y)
        cv2.line(image_with_grid, (0, y), (width, y), (255, 255, 0), 2)

    return image_with_grid


def find_lines(image, resolution=2, doVerbose=False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, resolution, np.pi / 180, 100, minLineLength=100, maxLineGap=150)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            if doVerbose:
                print(f"Line from ({x1}, {y1}) to ({x2}, {y2})")

    return image, lines


def find_intersection(l1, l2):
    x1, y1, x2, y2 = l1
    x3, y3, x4, y4 = l2
    if x1 == x2:
        # if the first line is vertical
        x = x1
        if x3 != x4:  # if the second line is not vertical
            slope2 = (y4 - y3) / (x4 - x3)
            y = slope2 * x + y3 - slope2 * x3
            return (int(x), int(y))
        else:
            return None
    elif x3 == x4:
        #  if the second line is vertical
        x = x3
        if x1 != x2:  # if the first line is not vertical
            slope1 = (y2 - y1) / (x2 - x1)
            y = slope1 * x + y1 - slope1 * x1
            return (int(x), int(y))
        else:
            return None
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0:
        return None
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
    return int(px), int(py)


def is_near_90_degrees(slope1, slope2, tolerance=5, zero_tolerance=1e-2):
    if (slope1 == np.inf and abs(slope2) <= zero_tolerance) or (slope2 == np.inf and abs(slope1) <= zero_tolerance):
        return True
    if (abs(slope1) <= zero_tolerance and slope2 == np.inf) or (abs(slope2) <= zero_tolerance and slope1 == np.inf):
        return True
    if slope1 == np.inf or slope2 == np.inf:
        return False

    angle = np.abs(np.arctan((slope2 - slope1) / (1 + slope1 * slope2)))
    angle_deg = np.degrees(angle)
    return 90 - tolerance <= angle_deg <= 90 + tolerance


def calculate_slope(line):
    x1, y1, x2, y2 = line
    if x2 - x1 != 0:
        return (y2 - y1) / (x2 - x1)
    else:
        return np.inf


# This takes the image finds the corner points
def find_corner_points_full(image, hsv_values, doVerbose=False):
    # Filter for red wall
    red_image = filter_image(image, hsv_values)
    # Clean up small defects
    # clean_image = clean_the_image(red_image)
    # Find the lines on the image
    edge_image, lines = find_lines(red_image)

    # lines = np.array(lines)
    # lines = lines.reshape(-1, 4)

    intersection_points = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            slope1 = calculate_slope(lines[i][0])
            slope2 = calculate_slope(lines[j][0])
            if is_near_90_degrees(slope1, slope2):
                intersection = find_intersection(lines[i][0], lines[j][0])
                if intersection:
                    intersection_points.append(intersection)
                    # print(f"Intersection point: {intersection}") 
                    cv2.circle(edge_image, intersection, radius=5, color=(255, 0, 0), thickness=-1)

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
            # closest_point = min(quadrants[q], key=lambda point: distance_between_points(point, (center_x, center_y)))
            closest_point = min(quadrants[q],
                                key=lambda point: np.sqrt((point[0] - center_x) ** 2 + (point[1] - center_y) ** 2))
            closest_points.append(closest_point)

    # An array of the 4 points in the corners
    final_points = np.array(closest_points, dtype="float32")

    # This is to print the images for visual inspection
    if doVerbose == True:
        images = [red_image, image, edge_image, image]
        printImagesFromWarping(images, final_points)

    return final_points


# This prints the images for visual inspection
def printImagesFromWarping(images, final_points):
    output_folder_path = 'images/outputObstacle/'

    red_image_path = output_folder_path + "red_image.jpg"
    cv2.imwrite(red_image_path, images[0])

    clean_image_path = output_folder_path + "clean_image.jpg"
    cv2.imwrite(clean_image_path, images[1])

    edge_image_path = output_folder_path + "edge_image.jpg"
    cv2.imwrite(edge_image_path, images[2])

    # Desired output size (dimensions in pixels for the warped image)
    dst_size = (1200, 1800)  # width, height
    gen_warped_image = warp_perspective(images[3], final_points, dst_size)

    gen_warped_image_path = output_folder_path + "gen_warped_image.jpg"
    cv2.imwrite(gen_warped_image_path, gen_warped_image)


def cluster_lines_into_4(image, lines):
    if lines is None or len(lines) == 0:
        print("No lines detected.")
        return

    lines = lines.reshape(-1, 4)

    angles = np.array([calculate_angle(line) for line in lines])
    midpoints = np.array([((x1 + x2) / 2, (y1 + y2) / 2) for x1, y1, x2, y2 in lines])
    # midpoints = np.array([(x1 + x2) / 2.0 for x1, y1, x2, y2 in lines]), np.array([(y1 + y2) / 2.0 for x1, y1, x2, y2 in lines])
    # midpoints = np.stack(midpoints, axis=1)

    angles = np.unwrap(angles[:, np.newaxis], axis=0)
    features = np.hstack((midpoints, angles))

    # kmeans = KMeans(n_clusters=4, random_state=42).fit(midpoints)
    kmeans = KMeans(n_clusters=4, random_state=42).fit(features)
    labels = kmeans.labels_

    averaged_lines = []
    for i in range(4):
        cluster_lines = lines[labels == i]

        avg_line = np.mean(cluster_lines, axis=0)
        averaged_lines.append(avg_line)

    if averaged_lines is not None:
        for x1, y1, x2, y2 in averaged_lines:
            cv2.line(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            print(f"Line from ({int(x1)}, {int(y1)}) to ({int(x2)}, {int(y2)})")

    return image
    # for x1, y1, x2, y2 in averaged_lines:
    #     print(f"Line from ({int(x1)}, {int(y1)}) to ({int(x2)}, {int(y2)})")


def calculate_angle(line):
    x1, y1, x2, y2 = line
    return np.arctan2(y2 - y1, x2 - x1)


def calculate_line_features(lines):
    """Calculate features for clustering: angle and distance from the origin."""
    angles = []
    distances = []
    for line in lines:
        x1, y1, x2, y2 = line
        angle = np.arctan2(y2 - y1, x2 - x1)
        distance = (y1 * x2 - y2 * x1) / np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        angles.append(angle)
        distances.append(distance)
    return np.array(angles), np.array(distances)


def cluster_lines(image, lines):
    angles, distances = calculate_line_features(lines.reshape(-1, 4))
    # Normalize angles to range [0, π] for undirected lines
    angles = np.mod(angles, np.pi)
    features = np.vstack((angles, distances)).T

    # K-means clustering
    kmeans = KMeans(n_clusters=4, random_state=42).fit(features)
    labels = kmeans.labels_

    # Prepare to average lines within each cluster
    averaged_lines = []
    for i in range(4):
        cluster_lines = lines[labels == i]
        # Average the coordinates of the lines in the cluster, if any
        if len(cluster_lines) > 0:
            avg_line = np.mean(cluster_lines.reshape(-1, 4), axis=0)
            averaged_lines.append(avg_line)
        else:
            print(f"No lines found for cluster {i}")

    # Print the averaged lines
    for line in averaged_lines:
        x1, y1, x2, y2 = line.astype(int)
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        print(f"Line from ({x1}, {y1}) to ({x2}, {y2})")

    return image


def are_points_close(point1, point2, tolerance=5):
    distance = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
    return distance <= tolerance

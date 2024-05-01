import cv2
import numpy as np

from src.client.field.robot import calc_vector_direction
from src.client.vision.filters import convert_hsv, filter_image_green, filter_image_red
from src.client.field.coordinate_system import find_corners
from src.client.vision.filters import apply_gray, apply_canny


def detect_robot(image):
    green_dot = detect_balls(filter_image_green(image),
                             min_radius=45, max_radius=50)
    if green_dot is None:  # TODO Proper error handling for green_dot
        print("No green dot.")

    red_dot = detect_balls(filter_image_red(image),
                           min_radius=45, max_radius=50)
    if red_dot is None:  # TODO Proper error handling for red_dot
        print("No red dot.")

    robot_pos = (red_dot[0][0], red_dot[0][1])
    robot_direction = calc_vector_direction(green_dot[0], robot_pos)

    return robot_pos, robot_direction

def detect_egg(image, min_radius=45,max_radius=55):
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
        print("balls count: ", len(circles))
    else:
        print("No balls detected.")

    return circles
def detect_balls(image, min_radius=15,max_radius=25):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection
    edges = cv2.Canny(gray, 110, 200)

    # Detect circles
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT,
                               dp=1.75, minDist=9,
                               param1=30, param2=35,
                               minRadius=min_radius, maxRadius=max_radius)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        print("balls count: ", len(circles))
    else:
        print("No balls detected.")

    return circles


class Shapes:  # TODO opløs Shapes klasse
    def __init__(self, image):
        self.original_image = image
        self.image = None
        self.detect_red_walls()
        self.image = apply_gray(image)
        self.circles = None
        self.lines = None

    #
    # def detect_balls(self):
    #     balls = 0
    #     rows = self.image.shape[0]
    #     blurred = apply_blur(self.image)
    #     self.circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, rows / 8, param1=100, param2=30, minRadius=10,
    #                                     maxRadius=100)
    #     if self.circles is not None:
    #         circles = np.round(self.circles[0, :]).astype("int")
    #         for (x, y, z) in circles:
    #             print('Ball:', str(balls))
    #             print('X:', x)
    #             print('Y:', y)
    #             print('Radius:', z)
    #             balls += 1
    #     return balls

    # def detect_ball(self):
    #     if len(self.image.shape) == 3 and self.image.shape[2] == 3:
    #         gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
    #     else:
    #         gray = self.image  # The image is already in grayscale
    #
    #     gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2, 2)
    #     circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 50, param1=100, param2=40, minRadius=0, maxRadius=0)
    #     if circles is not None:
    #         circles = np.uint16(np.around(circles))
    #         for i in circles[0, :]:
    #             return circles[0, 0]
    #     else:
    #         print("No ball detected")
    #         return None

    # def detect_balls(self):
    #     balls = 0
    #     rows = self.image.shape[0]
    #     blurred = apply_blur(self.image)
    #     self.circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1.5, rows / 5, param1=30, param2=35, minRadius=10,
    #                                     maxRadius=30)
    #     if self.circles is not None:
    #         circles = np.round(self.circles[0, :]).astype("int")
    #         for (x, y, z) in circles:
    #             print('Ball:', str(balls))
    #             print('X:', x)
    #             print('Y:', y)
    #             print('Radius:', z)
    #             balls += 1

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

    # def draw_corners_debug(self, image_to_draw_on):
    #     corners = find_corners(image_to_draw_on)
    #     if corners is not None:
    #         for corner in corners:
    #             x, y = tuple(corner.ravel())
    #             # cv2.circle(image_to_draw_on, (x, y), 5, (0, 255, 0), -1)  # Draw green circles at each corner

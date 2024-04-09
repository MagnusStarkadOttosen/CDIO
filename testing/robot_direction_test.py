import cv2
import unittest
# import sys
# import os

from src.client.field.robot import calc_degrees_to_rotate
from src.client.vision.shape_detection import detect_balls, _calc_robot_pos
from src.client.vision.filters import filter_image_green, filter_image_red

image = cv2.imread('images/robot_ball_90.jpeg')


class TestCalcDegrees(unittest.TestCase):
    def test_calc_degrees_to_rotate_hardcoded(self):
        degrees = calc_degrees_to_rotate((5, 5), (5, 8), (9, 5))
        expected_degrees = 90
        self.assertEqual(expected_degrees, degrees)

    def test_calc_degrees_from_image(self):
        green_dot = detect_balls(filter_image_green(image),
                                 min_radius=25, max_radius=35)
        if green_dot is None:
            print("No green dot.")
            return
        green_vector = (green_dot[0][0], green_dot[0][1])
        print(f"green_vector: {green_vector}")

        red_dot = detect_balls(filter_image_red(image),
                               min_radius=25, max_radius=35)
        if red_dot is None:
            print("No red dot.")
            return
        red_vector = (red_dot[0][0], red_dot[0][1])
        print(f"red_vect: {red_vector}")

        robot_pos = _calc_robot_pos(green_vector, red_vector)
        balls = detect_balls(image, min_radius=20)
        target_pos = (balls[0][0], balls[0][1])
        print(f"target_pos: {target_pos}")

        expected_degrees = 90
        actual_degrees = calc_degrees_to_rotate(robot_pos, green_vector, target_pos)
        print(actual_degrees)
        self.assertEqual(expected_degrees, actual_degrees)









#
# # Add the parent directory of 'src' to the Python path
# base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(base_path)
#
# #Manually placed corners on original image
# #corners = np.array([[417, 73], [1650, 66], [1689, 987], [403, 985]], dtype="float32") #Top left, top right, buttom right, buttom left
# corners = np.array([[393, 49], [1678, 42], [1723, 1005], [378, 1000]], dtype="float32")
#
# #Real world dimensions in cm
# real_world_size = (120, 180)  # height, width
#
# #Desired output size (dimensions in pixels for the warped image)
# dst_size = (1200, 1800)  # width, height
#
# #Path from where images comes from and path where the processed images are stored
# input_folder_path = 'images/'
# output_folder_path = 'images/'
#
# #Name of the image to be used
# image_name = 'robotdirection.jpeg'
# input_image_path = input_folder_path + image_name
# image = cv2.imread(input_image_path)




# if image is not None:
#
#     #Detecting the corners of the image
#
#     red_image = detect_red(image)
#     red_image_name = 'red_' + image_name
#     red_image_path = output_folder_path + red_image_name
#     cv2.imwrite(red_image_path, red_image)
#
#     green_image = detect_green(image)
#     green_image_name = 'green_' + image_name
#     green_image_path = output_folder_path + green_image_name
#     cv2.imwrite(green_image_path, green_image)
#
#     red_point = detect_ball(red_image)
#     green_point = detect_ball(green_image)
#
#     if red_image is not None:
#         if red_point is not None:
#             red_point_coordinates = (red_point[0], red_point[1])  # Extract x and y coordinates
#         else:
#             red_point_coordinates = None
#
#     if green_image is not None:
#         if green_point is not None:
#             green_point_coordinates = (green_point[0], green_point[1])  # Extract x and y coordinates
#         else:
#             green_point_coordinates = None
#
#         print("Red point coordinates:", red_point_coordinates)
#         print("Green point coordinates:", green_point_coordinates)

import cv2
import unittest
# import sys
# import os

from src.client.field.objects_on_field.robot import Robot
from src.client.vision.shape_detection import detect_balls

robot = Robot()
image = cv2.imread('images/image_with_robot.jpeg')
class TestUpdateRedAndGreenDot(unittest.TestCase):
    def test_update_red_and_green_dot(self):








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
input_image_path = input_folder_path + image_name
image = cv2.imread(input_image_path)




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

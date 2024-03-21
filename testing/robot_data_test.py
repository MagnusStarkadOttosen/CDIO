import cv2
import numpy as np
import sys
import os
import math

# Add the parent directory of 'src' to the Python path
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
from src.vision.detector_robot import *
from src.vision.shape_detection import *
from testing.visualization import draw_shapes
from src.vision.coordinate_system import *
from src.vision.filters import *
from src.client.robot_data import *




#Manually placed corners on original image
#corners = np.array([[417, 73], [1650, 66], [1689, 987], [403, 985]], dtype="float32") #Top left, top right, buttom right, buttom left
corners = np.array([[393, 49], [1678, 42], [1723, 1005], [378, 1000]], dtype="float32")

#Real world dimensions in cm
real_world_size = (120, 180)  # height, width

#Desired output size (dimensions in pixels for the warped image)
dst_size = (1200, 1800)  # width, height

#Path from where images comes from and path where the processed images are stored
input_folder_path = 'images/'
output_folder_path = 'images/'

#Name of the image to be used
image_name = 'test_robot.jpeg'
input_image_path = input_folder_path + image_name
image = cv2.imread(input_image_path)

if image is not None:
     #Detecting the corners of the image

    red_image = detect_red(image) 
    red_image_name = 'red_' + image_name
    red_image_path = output_folder_path + red_image_name
    cv2.imwrite(red_image_path, red_image)
    red_point = detect_ball(red_image)

    green_image = detect_green(image)
    green_image_name = 'green_' + image_name
    green_image_path = output_folder_path + green_image_name
    cv2.imwrite(green_image_path, green_image)
    green_point = detect_ball(green_image)    

   
   

    if red_image is not None:
        if red_point is not None:
            red_point_coordinates = (red_point[0], red_point[1])  # Extract x and y coordinates
        else:
            red_point_coordinates = None

    if green_image is not None:
        if green_point is not None:
            green_point_coordinates = (green_point[0], green_point[1])  # Extract x and y coordinates
        else:
            green_point_coordinates = None
    



    # print the red and green points' coordinates
    print(f"Red point coordinates: {red_point_coordinates}")
    print(f"Green point coordinates:{green_point_coordinates}")
    

    # distance from A to B
    distance = math.sqrt((green_point[0] - red_point[0]) ** 2 + (green_point[1] - red_point[1]) ** 2)
    print(f"Distance from A to B: {distance}")

    # distance from A to M :
    a = 8.5
    M = (red_point[0] + a / (distance * (green_point[0] - red_point[0])), red_point[1] + a / (distance * (green_point[1] - red_point[1])))
    print(f"The robot's position: {M}")

""""
    # distance from M to the target position
    distance_to_move = math.sqrt((target_point[0] - M[0]) ** 2 + (target_point[1] - M[1]) ** 2)
    print(f"Distance to move: {distance_to_move}")

    # the angle between the tector MB and tector MC with C is the ball's position
    pivot = get_degrees_toturn(M, target_point)
    print(f"The pivot: {pivot}")
"""
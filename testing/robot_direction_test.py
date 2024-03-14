import cv2
import numpy as np
from src.vision.detector_robot import *
from src.vision.shape_detection import Shapes
from testing.visualization import draw_shapes
from src.vision.coordinate_system import *
from src.vision.filters import *
from sklearn.cluster import KMeans


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
image_name = 'robotdirection.jpeg'
input_image_path = input_folder_path + image_name
image = cv2.imread(input_image_path)




if image is not None:
    
    #Detecting the corners of the image
    
    red_image = detect_red(image) 
    red_image_name = 'red_' + image_name
    red_image_path = output_folder_path + red_image_name
    cv2.imwrite(red_image_path, red_image)

    green_image = detect_green(image)
    green_image_name = 'green_' + image_name
    green_image_path = output_folder_path + green_image_name
    cv2.imwrite(green_image_path, green_image)

    red_point = detect_ball(red_image)
    green_point = detect_ball(green_image)

    print("Red point:", red_point)
    print("Green point:", green_point)

    

    print(f"Processed image done!") 
else:
    print("Error: Image not found. Please check the input folder path and image name.")


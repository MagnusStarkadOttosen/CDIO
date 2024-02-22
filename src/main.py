import cv2
import numpy as np

from camera.filters import apply_gray
#from ..testing.visualization import draw_circles, draw_lines, save_detection_image

#Path from where images comes from and path where the processed images are stored
input_folder_path = 'images/'
output_folder_path = 'images/'

#Name of the image to be used
image_name = '1.jpg'
input_image_path = input_folder_path + image_name

image = cv2.imread(input_image_path)
gray = apply_gray(image)
#save_detection_image(image)

#save_image("bowl', output_folder_path, image)
import cv2
import numpy as np

from src.vision.shape_detection import Shapes
from testing.visualization import draw_shapes

#Path from where images comes from and path where the processed images are stored
input_folder_path = 'images/'
output_folder_path = 'images/'

#Name of the image to be used
image_name = '1.jpg'
input_image_path = input_folder_path + image_name
image = cv2.imread(input_image_path)

if image is not None:
  shape_detector = Shapes(image)
  shape_detector.detect_balls()
  shape_detector.detect_walls()

  draw_shapes(shape_detector.circles, shape_detector.lines, image)

  output_image_name = 'processed_' + image_name
  output_image_path = output_folder_path + output_image_name
  cv2.imwrite(output_image_path, image)
  print(f"Processed image saved at: {output_image_path}") 

else:
  print("Error: Image not found. Please check the input folder path and image name.")

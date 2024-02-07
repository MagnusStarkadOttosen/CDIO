# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:18:10 2024

@author: MagnusStarkadOttosen
"""

import cv2
import numpy as np

input_folder_path = 'images/'

output_folder_path = 'images/'

image_name = '1.jpg'

input_image_path = input_folder_path + image_name

image = cv2.imread(input_image_path)

if image is not None:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    v = np.median(gray)
    sigma = 0.33
    
    lower_thresh = int(max(0, (1.0 - sigma) * v))
    upper_thresh = int(min(255, (1.0 + sigma) * v))
    
    canny = cv2.Canny(gray, lower_thresh, upper_thresh, 10)
    
    
    #median = cv2.medianBlur(gray,5)
    #blurred = cv2.GaussianBlur(median, (5, 5), 0)
    
    
    #thresh = cv2.threshold(blurred, 130 ,100, cv2.THRESH_BINARY_INV)[1]
    #canny = cv2.Canny(thresh, 255, 255, 10)
    
    output_image_name = 'processed_' + image_name

    output_image_path = output_folder_path + output_image_name

    cv2.imwrite(output_image_path, canny)
    print(f"Processed image saved at: {output_image_path}")
else:
    print("Error: Image not found. Please check the input folder path and image name.")

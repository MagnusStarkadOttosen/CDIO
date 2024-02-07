# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:18:10 2024

@author: MagnusStarkadOttosen
"""

import cv2
import numpy as np

#Path from where images comes from and path where the processed images are stored
input_folder_path = 'images/'
output_folder_path = 'images/'

#Name of the image to be used
image_name = '1.jpg'

input_image_path = input_folder_path + image_name

image = cv2.imread(input_image_path)

#Only proceed if an image is found
if image is not None:
    #Convert to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    #Compute the threashhold for the edge detection
    v = np.median(gray)
    sigma = 0.33
    lower_thresh = int(max(0, (1.0 - sigma) * v))
    upper_thresh = int(min(255, (1.0 + sigma) * v))
    
    #Edge detection
    canny = cv2.Canny(gray, lower_thresh, upper_thresh, 10)
    
    print("After Canny")
    
    #circles = cv2.HoughCircles(canny,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=5,maxRadius=0)
    
    median = cv2.medianBlur(gray,5)
    blurred = cv2.GaussianBlur(median, (5, 5), 0)
    
    
    rows = gray.shape[0]
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, rows / 8,param1=100, param2=30,minRadius=10, maxRadius=100)

    print("Before If")

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv2.circle(image, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv2.circle(image, center, radius, (255, 0, 255), 3)
    
    print("After if")
    

    linesP = cv2.HoughLinesP(canny, 1, np.pi / 180, 50, None, 50, 10)
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(image, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
    
    #median = cv2.medianBlur(gray,5)
    #blurred = cv2.GaussianBlur(median, (5, 5), 0)
    #thresh = cv2.threshold(blurred, 130 ,100, cv2.THRESH_BINARY_INV)[1]
    #canny = cv2.Canny(thresh, 255, 255, 10)
    
    #Name the output image and saved to the output folder
    output_image_name = 'processed_' + image_name
    output_image_path = output_folder_path + output_image_name
    cv2.imwrite(output_image_path, image)
    print(f"Processed image saved at: {output_image_path}")
else:
    print("Error: Image not found. Please check the input folder path and image name.")

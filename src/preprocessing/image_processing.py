import cv2
import numpy as np
import os

# path to the image
image_path = "/Users/lynguyenhansen/Documents/GitHub/CDIO/originalImages/Image 1.jpeg"

# read the image
image = cv2.imread(image_path)

# convert the image to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# define the range of white color in HSV
white_lower = np.array([0, 0, 200])
white_upper = np.array([180, 30, 255])
orange_lower = np.array([5, 150, 150])
orange_upper = np.array([15, 255, 255])

# create a mask for the white color
white_mask = cv2.inRange(hsv, white_lower, white_upper)
orange_mask = cv2.inRange(hsv, orange_lower, orange_upper)

# find contours in the mask
white_contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
orange_contours, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# create a directory to save the extracted images
output_dir = 'extracted_images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# function to save the contours as images
def save_contours(contours, color_name, min_area=50, max_area=1000):
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            if 0.8 < aspect_ratio < 1.2:  # filter out non-circular objects
                roi = image[y:y+h, x:x+w]
                output_path = os.path.join(output_dir, f"{color_name}_{i}.png")
                cv2.imwrite(output_path, roi)

# save the extracted images
save_contours(white_contours, 'white_ball')
save_contours(orange_contours, 'orange_ball')

print("Extracted and saved objects from the original image")

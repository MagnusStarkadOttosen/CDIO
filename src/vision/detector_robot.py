import cv2
import numpy as np
from src.vision.filters import apply_blur

def detect_ball(image):
        # from image_detection import detect_red and detect_green functions 
        #give the robot position with red point's coordinates and green point's coordinates
        
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2,2)
    # center=(0,0)
    # edges = cv2.Canny(image, 50, 150, apertureSize=3)
    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 50, param1=100, param2=40, minRadius=0, maxRadius=0)
    if circles is not None:
 
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            print(f"circle center: x={i[0]}, y={i[1]}")
        return circles[0,0]
    else:
        print("No ball detected")
        return None


       
    

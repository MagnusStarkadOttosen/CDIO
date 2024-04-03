import cv2
import numpy as np
from src.vision.filters import *

def detect_ball(image):
    balls=0
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # Apply edge detection
    edges = cv2.Canny(gray, 100, 200)



    # Detect circles
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1.75, minDist=14, param1=30, param2=35, minRadius=10, maxRadius=30)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for idx, (x, y, r) in enumerate(circles[0, :]):
            # Draw the outer circle
            cv2.circle(image, (x, y), r, (128, 0, 128), 2)
            # Draw the center of the circle
            cv2.circle(image, (x, y), 2, (128, 0, 128), 3)
            # Enumerate the detected balls
            cv2.putText(image, str(idx + 1), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, z) in circles:
                    print('Ball:', str(balls))
                    print('X:', x)
                    print('Y:', y)
                    print('Radius:', z)
                    balls += 1
    else:
        print("No balls detected.")
    return image, circles



def detect_ballsFirst(image):
    balls = 0
    rows = image.shape[0]
    gray = apply_gray(image)
    blurred = apply_blur(gray)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, rows / 8, param1=100, param2=30, minRadius=10,
                                    maxRadius=100)
    if circles is not None:

        circles = np.round(circles[0, :]).astype("int")
        for (x, y, z) in circles:
            print('Ball:', str(balls))
            print('X:', x)
            print('Y:', y)
            print('Radius:', z)
            balls += 1
    return circles


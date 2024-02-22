import cv2
import numpy as np

from src.camera.filters import apply_canny, apply_blur

def detect_balls(image): #IMAGE NEEDS TO BE FILTERS GRAY
  rows = image.shape[0]
  blurred = apply_blur(image)
  circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, rows / 8,param1=100, param2=30,minRadius=10, maxRadius=100)

def detect_walls(image): 
   canny = apply_canny(image)
   linesP = cv2.HoughLinesP(canny, 1, np.pi / 180, 50, None, 50, 10)
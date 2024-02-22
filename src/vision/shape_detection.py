import cv2
import numpy as np

from src.camera.filters import apply_gray, apply_canny, apply_blur

class Shapes:
   def __init__(self, image):
      self.image = apply_gray(image)
      self.circles = None
      self.lines = None

   def detect_balls(self):
      rows = self.image.shape[0]
      blurred = apply_blur(self.image)
      self.circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, rows / 8,param1=100, param2=30,minRadius=10, maxRadius=100)

   def detect_walls(self): 
      canny = apply_canny(self.image)
      self.lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 50, None, 50, 10)
   
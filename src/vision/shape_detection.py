import cv2
import numpy as np

from src.vision.filters import apply_gray, apply_canny, apply_blur, convert_hsv

class Shapes:
   def __init__(self, image):
      self.original_image  = image
      self.image = None
      self.detect_red_walls()
      self.image = apply_gray(image)
      self.circles = None
      self.lines = None

   def detect_balls(self):
      balls = 0
      rows = self.image.shape[0]
      blurred = apply_blur(self.image)
      self.circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, rows / 8,param1=100, param2=30,minRadius=10, maxRadius=100)
      if self.circles is not None:
         circles = np.round(self.circles[0, :]).astype("int")
         for (x, y, z) in circles:
            print('Ball:', str(balls))
            print('X:', x)
            print('Y:', y)
            print('Radius:', z)
            balls += 1

   def detect_walls(self): 
      canny = apply_canny(self.image)
      self.lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 50, None, 50, 10)
   
   def detect_red_walls(self):
      hsv = convert_hsv(self.original_image)
      lower_red1 = np.array([0, 70, 50])
      upper_red1 = np.array([10, 255, 255])
      lower_red2 = np.array([170, 70, 50])
      upper_red2 = np.array([180, 255, 255])
      
      mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
      mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
      mask = cv2.bitwise_or(mask1, mask2)

      self.image = cv2.bitwise_and(self.original_image, self.original_image, mask=mask)
      
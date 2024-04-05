import cv2
import numpy as np

def apply_gray(image):
   gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   print("After gray")
   
   return gray

def apply_canny(image):
   #Compute the threshhold for the edge detection
    v = np.median(image)
    sigma = 0.33
    lower_thresh = int(max(0, (1.0 - sigma) * v))
    upper_thresh = int(min(255, (1.0 + sigma) * v))
      
    #Edge detection
    canny = cv2.Canny(image, lower_thresh, upper_thresh, 10)
    print("After canny")
    return canny

def apply_blur(image):
  median = cv2.medianBlur(image,5)
  print("after median")

  blurred = cv2.GaussianBlur(median, (5, 5), 0)
  print("after blurred")

  return blurred

def convert_hsv(image):
   hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
   return hsv
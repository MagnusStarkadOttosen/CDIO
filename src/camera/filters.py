import cv2
import numpy as np

def filter_image(input_image_path):
  image = cv2.imread(input_image_path)
  #Only proceed if an image is found
  if image is not None:
      #Convert to gray scale
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      print("After gray")
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
      print("after median")
      blurred = cv2.GaussianBlur(median, (5, 5), 0)
      print("after blurred")
      return blurred
  else:
    print("Error: Image not found. Please check the input folder path and image name.")


def save_image(image_name, output_folder_path, image):
    output_image_name = 'processed_' + image_name
    output_image_path = output_folder_path + output_image_name
    print(output_image_path)
    cv2.imwrite(output_image_path, image)
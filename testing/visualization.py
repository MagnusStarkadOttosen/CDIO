import cv2
import numpy as np

from src.camera.object_detection import detect_balls, detect_walls

def generate_circles(image):
  circles = generate_circles(image)
  if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        center = (i[0], i[1])
        # circle center
        cv2.circle(image, center, 1, (0, 100, 100), 3)
        # circle outline
        radius = i[2]
        cv2.circle(image, center, radius, (255, 0, 255), 3)

def generate_lines(image):
  linesP = generate_lines(image)
  if linesP is not None:
      for i in range(0, len(linesP)):
          l = linesP[i][0]
          cv2.line(image, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)
  else:
    print("Lines are empty.")

def save_detection_image(image_name, output_folder_path, image):
  output_image_name = 'processed_' + image_name
  output_image_path = output_folder_path + output_image_name
  cv2.imwrite(output_image_path, image)
  print(f"Processed image saved at: {output_image_path}")

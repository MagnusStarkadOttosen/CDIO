import cv2
import numpy as np

def draw_shapes(circles, linesP, image):
   draw_circles(circles, image)
   draw_lines(linesP, image)
   #return image
   
def draw_circles(circles, image):
  #circles = detect_balls(image)
  if circles is not None:
    circles = np.uint16(np.around(circles))
    ball_num = 0
    for i in circles[0, :]:
        center = (i[0], i[1])
        # circle center
        cv2.circle(image, center, 1, (0, 100, 100), 3)
        # circle outline
        radius = i[2]
        cv2.circle(image, center, radius, (255, 0, 255), 3)
        cv2.putText(image, str(ball_num), center, fontFace = cv2.FONT_HERSHEY_COMPLEX, fontScale = 1.5, color = (255, 0, 255))
        ball_num += 1
  else:
     print("Circles are empty.")
  

def draw_lines(linesP, image):
  #linesP = detect_walls(image)
  if linesP is not None:
      for i in range(0, len(linesP)):
          l = linesP[i][0]
          cv2.line(image, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)
  else:
    print("Lines are empty.")


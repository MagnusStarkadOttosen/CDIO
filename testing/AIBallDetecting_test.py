import math
import os
import sys
import cv2
import numpy as np
import time
from src.client.vision.AIBallDetection import detect_balls_with_model

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.client.field.coordinate_system import find_corner_points_full, warp_perspective
from src.client.hsvLoad import read_hsv_values




CAM_INDEX = 2


# Capture from camera
cap = cv2.VideoCapture(CAM_INDEX,cv2.CAP_DSHOW)
dst_size = (1200, 1800)
ret, frame = cap.read()


red_hsv_values = read_hsv_values('hsv_presets_red.txt')
final_points = find_corner_points_full(frame, red_hsv_values, doVerbose=True)

# cv2.namedWindow('warped', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('warped', 1200, 1800)

last_detection_time = time.time()
detection_interval = 1  # seconds

gen_warped_frame = warp_perspective(frame, final_points, dst_size)
white_balls, orange_balls = detect_balls_with_model(gen_warped_frame)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    gen_warped_frame = warp_perspective(frame, final_points, dst_size)

    current_time = time.time()
    if current_time - last_detection_time >= detection_interval:
        white_balls, orange_balls = detect_balls_with_model(gen_warped_frame)
        if white_balls is not None:
            print(f"White balls: {white_balls}")
        if orange_balls is not None:
            print(f"Orange balls: {orange_balls}")

    

    # for ball in white_balls:
    #     x, y, r = ball
    #     # Draw the circle
    #     cv2.circle(gen_warped_frame, (x, y), r, (0, 255, 0), 2)
    #     # Put the label near the circle
    #     label = f"white_ball"
    #     cv2.putText(gen_warped_frame, label, (x - r, y - r - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # for ball in orange_balls:
    #     x, y, r = ball
    #     # Draw the circle
    #     cv2.circle(gen_warped_frame, (x, y), r, (0, 0, 255), 2)
    #     # Put the label near the circle
    #     label = f"orange_ball"
    #     cv2.putText(gen_warped_frame, label, (x - r, y - r - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # cv2.imshow('warped', gen_warped_frame)
        last_detection_time = current_time
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import cv2
import numpy as np

def detect_ball(image):
    balls=0
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection
    edges = cv2.Canny(gray, 100, 200)

    # Detect circles
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1.75, minDist=7, param1=30, param2=35, minRadius=10, maxRadius=30)
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

# import cv2
# import numpy as np
# from src.vision.filters import apply_blur
#
# def detect_ball(image):
#         # from image_detection import detect_red and detect_green functions
#         #give the robot position with red point's coordinates and green point's coordinates
#
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2,2)
#     # center=(0,0)
#     # edges = cv2.Canny(image, 50, 150, apertureSize=3)
#     circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 50, param1=100, param2=40, minRadius=0, maxRadius=0)
#     if circles is not None:
#         circles = np.uint16(np.around(circles))
#         for i in circles[0, :]:
#             # print(f"circle center: x={i[0]}, y={i[1]}")
#             return circles[0,0]
#     else:
#         print("No ball detected")
#         return None
#
import cv2
import numpy as np


# def detect_ball(image):
#     balls = 0
#     # Convert to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # Apply edge detection
#     edges = cv2.Canny(gray, 100, 200)
#
#     # Detect circles
#     circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1.75, minDist=7, param1=30, param2=35, minRadius=10,
#                                maxRadius=30)
#     if circles is not None:
#         circles = np.uint16(np.around(circles))
#         for i in circles[0, :]:
#             # Draw the outer circle
#             cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
#             # Draw the center of the circle
#             cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)
#
#         circles = np.round(circles[0, :]).astype("int")
#         for (x, y, z) in circles:
#             print('Ball:', str(balls))
#             print('X:', x)
#             print('Y:', y)
#             print('Radius:', z)
#             balls += 1
#     return image, circles
#


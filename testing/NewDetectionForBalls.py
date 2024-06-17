import cv2
import numpy as np

# Load the image
image = cv2.imread('originalImages/PreWarpedCourse.jpg')

# Convert the image to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define color ranges for white and orange in HSV space
# Adjust the ranges as needed based on your image
white_lower = np.array([0, 0, 222])
white_upper = np.array([179, 54, 255])
orange_lower = np.array([9, 28, 231])
orange_upper = np.array([30, 255, 255])

# Create masks for white and orange
mask_white = cv2.inRange(hsv, white_lower, white_upper)
mask_orange = cv2.inRange(hsv, orange_lower, orange_upper)

# Combine the masks
mask = cv2.bitwise_or(mask_white, mask_orange)

# Apply morphological operations to remove noise and fill holes
kernel = np.ones((5, 5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours by radius to detect balls
min_radius = 15  # Minimum radius of the balls
max_radius = 25  # Maximum radius of the balls
balls = []

for contour in contours:
    ((x, y), radius) = cv2.minEnclosingCircle(contour)
    if min_radius < radius < max_radius:
        center = (int(x), int(y))
        radius = int(radius)
        # Draw the detected ball on the original image
        cv2.circle(image, center, radius, (0, 255, 0), 2)
        balls.append((center, radius))

# Save or display the results
cv2.imwrite('detected_balls.png', image)
cv2.imshow('Detected Balls', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
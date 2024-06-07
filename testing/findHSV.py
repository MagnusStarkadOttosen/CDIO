import cv2
import numpy as np

def nothing(x):
    pass

# Capture from camera
cap = cv2.VideoCapture(2)

# Create a window
cv2.namedWindow('image')

# Create trackbars for color change
cv2.createTrackbar('LowerH', 'image', 0, 179, nothing)
cv2.createTrackbar('LowerS', 'image', 0, 255, nothing)
cv2.createTrackbar('LowerV', 'image', 0, 255, nothing)
cv2.createTrackbar('UpperH', 'image', 0, 179, nothing)
cv2.createTrackbar('UpperS', 'image', 0, 255, nothing)
cv2.createTrackbar('UpperV', 'image', 0, 255, nothing)

while(True):
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get info from track bar
    lh = cv2.getTrackbarPos('LowerH', 'image')
    ls = cv2.getTrackbarPos('LowerS', 'image')
    lv = cv2.getTrackbarPos('LowerV', 'image')
    uh = cv2.getTrackbarPos('UpperH', 'image')
    us = cv2.getTrackbarPos('UpperS', 'image')
    uv = cv2.getTrackbarPos('UpperV', 'image')

    # Set the lower and upper HSV range according to the value selected
    # by the trackbar
    lower_bound = np.array([lh, ls, lv])
    upper_bound = np.array([uh, us, uv])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Display result
    cv2.imshow('image', res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
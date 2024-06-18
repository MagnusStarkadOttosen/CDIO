import cv2
import numpy as np

def normalize_image(image):
    """
    Normalize the image to a standard scale.
    """
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Normalize the grayscale image
    norm_image = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

    # Convert back to BGR for further processing
    normalized_image = cv2.cvtColor(norm_image, cv2.COLOR_GRAY2BGR)
    
    return normalized_image

def detect_balls(image, lower_hsv, upper_hsv, min_radius=15, max_radius=25):
    """
    Detect balls in the image using HoughCircles.
    """
    # Convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Apply color thresholding
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    
    # Convert to grayscale
    gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)

    # Apply blur
    blur = cv2.GaussianBlur(gray, (9, 9), 2)

    # Apply edge detection
    edges = cv2.Canny(blur, 50, 150)

    # Detect circles
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT,
                               dp=1.75, minDist=9,
                               param1=30, param2=35,
                               minRadius=min_radius, maxRadius=max_radius)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        return circles, masked_image

    return [], masked_image

# Create trackbars for adjusting HSV thresholds
def nothing(x):
    pass

cv2.namedWindow('HSV Thresholds', cv2.WINDOW_NORMAL)  # Create a resizable window
cv2.resizeWindow('HSV Thresholds', 600, 400)  # Resize the window to make sliders visible

# Define initial color ranges for white and orange
initial_lower_white = [0, 0, 200]
initial_upper_white = [179, 30, 255]
initial_lower_orange = [10, 100, 100]
initial_upper_orange = [25, 255, 255]

# Create trackbars for white ball thresholds
cv2.createTrackbar('LowerH White', 'HSV Thresholds', initial_lower_white[0], 179, nothing)
cv2.createTrackbar('LowerS White', 'HSV Thresholds', initial_lower_white[1], 255, nothing)
cv2.createTrackbar('LowerV White', 'HSV Thresholds', initial_lower_white[2], 255, nothing)
cv2.createTrackbar('UpperH White', 'HSV Thresholds', initial_upper_white[0], 179, nothing)
cv2.createTrackbar('UpperS White', 'HSV Thresholds', initial_upper_white[1], 255, nothing)
cv2.createTrackbar('UpperV White', 'HSV Thresholds', initial_upper_white[2], 255, nothing)

# Create trackbars for orange ball thresholds
cv2.createTrackbar('LowerH Orange', 'HSV Thresholds', initial_lower_orange[0], 179, nothing)
cv2.createTrackbar('LowerS Orange', 'HSV Thresholds', initial_lower_orange[1], 255, nothing)
cv2.createTrackbar('LowerV Orange', 'HSV Thresholds', initial_lower_orange[2], 255, nothing)
cv2.createTrackbar('UpperH Orange', 'HSV Thresholds', initial_upper_orange[0], 179, nothing)
cv2.createTrackbar('UpperS Orange', 'HSV Thresholds', initial_upper_orange[1], 255, nothing)
cv2.createTrackbar('UpperV Orange', 'HSV Thresholds', initial_upper_orange[2], 255, nothing)

# Capture from camera
cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Get current positions of the trackbars for white ball thresholds
    lower_white = np.array([cv2.getTrackbarPos('LowerH White', 'HSV Thresholds'),
                            cv2.getTrackbarPos('LowerS White', 'HSV Thresholds'),
                            cv2.getTrackbarPos('LowerV White', 'HSV Thresholds')])
    upper_white = np.array([cv2.getTrackbarPos('UpperH White', 'HSV Thresholds'),
                            cv2.getTrackbarPos('UpperS White', 'HSV Thresholds'),
                            cv2.getTrackbarPos('UpperV White', 'HSV Thresholds')])

    # Get current positions of the trackbars for orange ball thresholds
    lower_orange = np.array([cv2.getTrackbarPos('LowerH Orange', 'HSV Thresholds'),
                             cv2.getTrackbarPos('LowerS Orange', 'HSV Thresholds'),
                             cv2.getTrackbarPos('LowerV Orange', 'HSV Thresholds')])
    upper_orange = np.array([cv2.getTrackbarPos('UpperH Orange', 'HSV Thresholds'),
                             cv2.getTrackbarPos('UpperS Orange', 'HSV Thresholds'),
                             cv2.getTrackbarPos('UpperV Orange', 'HSV Thresholds')])

    # Normalize the image for white ball detection
    normalized_image = normalize_image(frame)
    
    # Detect white balls
    white_circles, white_masked_image = detect_balls(normalized_image, lower_white, upper_white)
    white_ball_count = len(white_circles)
    
    # Detect orange balls using the original image
    orange_circles, orange_masked_image = detect_balls(frame, lower_orange, upper_orange)
    orange_ball_count = len(orange_circles)
    
    # Display circles for white balls
    for (x, y, r) in white_circles:
        cv2.circle(frame, (x, y), r, (255, 255, 255), 4)
    
    # Display circles for orange balls
    for (x, y, r) in orange_circles:
        cv2.circle(frame, (x, y), r, (0, 165, 255), 4)
    
    # Display ball counts
    cv2.putText(frame, f"White balls detected: {white_ball_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Orange balls detected: {orange_ball_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
    
    # Display results
    cv2.imshow('Detected Balls', frame)
    cv2.imshow('White Masked Image', white_masked_image)
    cv2.imshow('Orange Masked Image', orange_masked_image)
    cv2.imshow('Normalized Image', normalized_image)  # Show the normalized image used for white ball detection

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

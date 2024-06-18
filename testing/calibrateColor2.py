import cv2
import numpy as np
import os

def read_hsv_values(filename):
    hsv_values = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split()
            hsv_values[key] = int(value)
    return hsv_values

def adaptive_threshold(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY, 11, 2)
    return adaptive_thresh

def segment_image(image):
    height, width, _ = image.shape
    shaded_region = image[:, :width // 2]
    bright_region = image[:, width // 2:]
    return shaded_region, bright_region

def apply_hsv_filter(image, lower_bound, upper_bound):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    result = cv2.bitwise_and(image, image, mask=mask)
    return result

def detect_balls(image, min_radius=15, max_radius=25):
    normalized_image = normalize_image(image)
    gray = cv2.cvtColor(normalized_image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 2)
    edges = cv2.Canny(blur, 50, 150)
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT,
                               dp=1.75, minDist=9,
                               param1=30, param2=35,
                               minRadius=min_radius, maxRadius=max_radius)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        return circles
    return []

def normalize_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    norm_image = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    normalized_image = cv2.cvtColor(norm_image, cv2.COLOR_GRAY2BGR)
    return normalized_image

def save_color_presets(color, lower_bound, upper_bound, base_filename="hsv_presets"):
    filename = f"{base_filename}_{color}.txt"
    with open(filename, "w") as file:
        file.write(f"LowerH {lower_bound[0]}\n")
        file.write(f"LowerS {lower_bound[1]}\n")
        file.write(f"LowerV {lower_bound[2]}\n")
        file.write(f"UpperH {upper_bound[0]}\n")
        file.write(f"UpperS {upper_bound[1]}\n")
        file.write(f"UpperV {upper_bound[2]}\n")
    print(f"{color.capitalize()} HSV values saved to {filename}")

def load_color_presets(color, base_filename="hsv_presets"):
    filename = f"{base_filename}_{color}.txt"
    if os.path.isfile(filename):
        with open(filename, "r") as file:
            lines = file.readlines()
            lower_bound = np.array([int(lines[0].split()[1]), int(lines[1].split()[1]), int(lines[2].split()[1])])
            upper_bound = np.array([int(lines[3].split()[1]), int(lines[4].split()[1]), int(lines[5].split()[1])])
        print(f"{color.capitalize()} HSV values loaded from {filename}")
        return lower_bound, upper_bound
    else:
        print(f"File {filename} not found. Using default values.")
        return None, None

def warp_perspective(image, points, dst_size):
    src_points = np.array(points, dtype='float32')
    dst_points = np.array([[0, 0], [dst_size[0] - 1, 0], [dst_size[0] - 1, dst_size[1] - 1], [0, dst_size[1] - 1]], dtype='float32')
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    warped = cv2.warpPerspective(image, matrix, dst_size)
    return warped

def nothing(x):
    pass

# Initialize camera
cam_index = 2
cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
output_dir = 'images/outputCalibrate'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load default HSV values
lower_bound_default, upper_bound_default = load_color_presets("default")
if lower_bound_default is None or upper_bound_default is None:
    lower_bound_default = np.array([0, 0, 0])
    upper_bound_default = np.array([179, 255, 255])

# Create windows
cv2.namedWindow('Lower Bounds')
cv2.namedWindow('Upper Bounds')
cv2.namedWindow('Result')
cv2.namedWindow('Normalized Image')
cv2.namedWindow('Warped')
cv2.namedWindow('Combined Result')

# Create trackbars for color adjustment
cv2.createTrackbar('LowerH', 'Lower Bounds', lower_bound_default[0], 179, nothing)
cv2.createTrackbar('LowerS', 'Lower Bounds', lower_bound_default[1], 255, nothing)
cv2.createTrackbar('LowerV', 'Lower Bounds', lower_bound_default[2], 255, nothing)
cv2.createTrackbar('UpperH', 'Upper Bounds', upper_bound_default[0], 179, nothing)
cv2.createTrackbar('UpperS', 'Upper Bounds', upper_bound_default[1], 255, nothing)
cv2.createTrackbar('UpperV', 'Upper Bounds', upper_bound_default[2], 255, nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Apply adaptive threshold
    adaptive_thresh = adaptive_threshold(frame)

    # Segment the image into shaded and bright regions
    shaded_region, bright_region = segment_image(frame)

    # Apply HSV filters
    lower_bound = np.array([cv2.getTrackbarPos('LowerH', 'Lower Bounds'),
                            cv2.getTrackbarPos('LowerS', 'Lower Bounds'),
                            cv2.getTrackbarPos('LowerV', 'Lower Bounds')])
    upper_bound = np.array([cv2.getTrackbarPos('UpperH', 'Upper Bounds'),
                            cv2.getTrackbarPos('UpperS', 'Upper Bounds'),
                            cv2.getTrackbarPos('UpperV', 'Upper Bounds')])
    shaded_filtered = apply_hsv_filter(shaded_region, lower_bound, upper_bound)
    bright_filtered = apply_hsv_filter(bright_region, lower_bound, upper_bound)

    # Detect balls in both regions
    shaded_circles = detect_balls(shaded_filtered)
    bright_circles = detect_balls(bright_filtered)

    # Combine results
    combined_frame = np.hstack((shaded_filtered, bright_filtered))
    combined_circles = []

    if shaded_circles is not None:
        combined_circles.extend(shaded_circles)
    if bright_circles is not None:
        combined_circles.extend(bright_circles)
    combined_circles = np.array(combined_circles)

    if combined_circles is not None and combined_circles.size > 0:
        for (x, y, r) in combined_circles:
            cv2.circle(combined_frame, (x, y), r, (255, 255, 0), 4)

    # Display the combined result
    cv2.imshow('Combined Result', combined_frame)

    # Warping Perspective
    points = [(50, 50), (frame.shape[1] - 50, 50), (frame.shape[1] - 50, frame.shape[0] - 50), (50, frame.shape[0] - 50)]
    warped_frame = warp_perspective(frame, points, (1200, 800))
    cv2.imshow('Warped', warped_frame)

    # Display the normalized image
    normalized_image = normalize_image(combined_frame)
    cv2.imshow('Normalized Image', normalized_image)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        save_color_presets("default", lower_bound, upper_bound)

cap.release()
cv2.destroyAllWindows()

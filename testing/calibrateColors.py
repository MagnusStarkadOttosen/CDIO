import os
import sys
import cv2
import numpy as np

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.client.field.coordinate_system import find_corner_points_full, warp_perspective

def find_lines(image, resolution=1, doVerbose=False):
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, resolution, np.pi/180, 100, minLineLength=100, maxLineGap=150)
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            if doVerbose:
                print(f"Line from ({x1}, {y1}) to ({x2}, {y2})")

    return image, lines

def detect_balls(image, min_radius=15,max_radius=25):
    #normalized = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX)
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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
        return circles

    return []

def nothing(x):
    pass

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

# Capture from camera
cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
dst_size = (1200, 1800)
ret, frame = cap.read()

lower_bound, upper_bound = load_color_presets("default")
final_points = find_corner_points_full(frame, doVerbose=True)

# Create windows
cv2.namedWindow('Lower Bounds')
cv2.namedWindow('Upper Bounds')
cv2.namedWindow('Result')
cv2.namedWindow('warped')

# Color presets and current color
colors = {
    'green': {'LowerH': 35, 'LowerS': 100, 'LowerV': 100, 'UpperH': 85, 'UpperS': 255, 'UpperV': 255},
    'red': {'LowerH': 0, 'LowerS': 100, 'LowerV': 100, 'UpperH': 10, 'UpperS': 255, 'UpperV': 255},
    'orange': {'LowerH': 10, 'LowerS': 100, 'LowerV': 100, 'UpperH': 25, 'UpperS': 255, 'UpperV': 255},
    'white': {'LowerH': 0, 'LowerS': 0, 'LowerV': 200, 'UpperH': 179, 'UpperS': 30, 'UpperV': 255}
}
current_color = 'green'

# Toggle for circles and lines
show_circles = False
show_lines = False


# Initialize trackbars for the initial color (green)
for k, v in colors[current_color].items():
    window = 'Lower Bounds' if 'Lower' in k else 'Upper Bounds'
    cv2.createTrackbar(k, window, v, 179 if 'H' in k else 255, nothing)
    
# Load saved presets if available
# lower_bound, upper_bound = load_color_presets(current_color)
lower_bound, upper_bound = load_color_presets("default")
if lower_bound is not None and upper_bound is not None:
    cv2.setTrackbarPos('LowerH', 'Lower Bounds', lower_bound[0])
    cv2.setTrackbarPos('LowerS', 'Lower Bounds', lower_bound[1])
    cv2.setTrackbarPos('LowerV', 'Lower Bounds', lower_bound[2])
    cv2.setTrackbarPos('UpperH', 'Upper Bounds', upper_bound[0])
    cv2.setTrackbarPos('UpperS', 'Upper Bounds', upper_bound[1])
    cv2.setTrackbarPos('UpperV', 'Upper Bounds', upper_bound[2])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to HSV and get trackbar positions
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([cv2.getTrackbarPos('LowerH', 'Lower Bounds'), cv2.getTrackbarPos('LowerS', 'Lower Bounds'), cv2.getTrackbarPos('LowerV', 'Lower Bounds')])
    upper_bound = np.array([cv2.getTrackbarPos('UpperH', 'Upper Bounds'), cv2.getTrackbarPos('UpperS', 'Upper Bounds'), cv2.getTrackbarPos('UpperV', 'Upper Bounds')])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    
    gen_warped_frame = warp_perspective(res, final_points, dst_size)

    # Display lines
    if show_lines:
        lines = find_lines(res)
    
    # Detect and count balls
    circles = detect_balls(res)
    ball_count = len(circles)
    circles2 = detect_balls(gen_warped_frame)
    ball_count2 = len(circles2)
    
    # Display circles
    if circles is not None and show_circles:
        for (x, y, r) in circles:
            cv2.circle(res, (x, y), r, (255, 255, 0), 4)
    # Display circles
    if circles2 is not None and show_circles:
        for (x, y, r) in circles2:
            cv2.circle(gen_warped_frame, (x, y), r, (255, 255, 0), 4)      
    
    cv2.putText(res, f"Balls detected: {ball_count}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(gen_warped_frame, f"Balls detected: {ball_count2}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Result', res)
    cv2.imshow('warped', gen_warped_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        save_color_presets(current_color, lower_bound, upper_bound)
    elif key == ord('c'): # Toggle circles
        show_circles = not show_circles
    elif key == ord('l'): # Toggle lines
        show_lines = not show_lines
    elif key in [ord('g'), ord('r'), ord('o'), ord('w')]:  # Preset selection keys
        preset_keys = {'g': 'green', 'r': 'red', 'o': 'orange', 'w': 'white'}
        current_color = preset_keys[chr(key)]
        for k in colors[current_color]:
            window = 'Lower Bounds' if 'Lower' in k else 'Upper Bounds'
            cv2.setTrackbarPos(k, window, colors[current_color][k])
        # Load saved presets if available
        lower_bound, upper_bound = load_color_presets(current_color)
        if lower_bound is not None and upper_bound is not None:
            cv2.setTrackbarPos('LowerH', 'Lower Bounds', lower_bound[0])
            cv2.setTrackbarPos('LowerS', 'Lower Bounds', lower_bound[1])
            cv2.setTrackbarPos('LowerV', 'Lower Bounds', lower_bound[2])
            cv2.setTrackbarPos('UpperH', 'Upper Bounds', upper_bound[0])
            cv2.setTrackbarPos('UpperS', 'Upper Bounds', upper_bound[1])
            cv2.setTrackbarPos('UpperV', 'Upper Bounds', upper_bound[2])

cap.release()
cv2.destroyAllWindows()

import math
import os
import sys
import cv2
import numpy as np

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.client.field.coordinate_system import calculate_slope, find_corner_points_full, find_intersection, is_near_90_degrees, warp_perspective

warp = True
edges = False
CAM_INDEX = 2

def read_hsv_values(filename):
    hsv_values = {}
    # temp = "C:/Users/bayou/PycharmProjects/CDIO/hsv_presets_red.txt"
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split()
            hsv_values[key] = int(value)
    return hsv_values

def find_lines(image, resolution=1, doVerbose=False):
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    kernel = np.ones((3, 3), np.uint8)  # You can adjust the kernel size as needed
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)

    lines = cv2.HoughLinesP(dilated_edges, resolution, np.pi/180, 100, minLineLength=100, maxLineGap=150)
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            if doVerbose:
                print(f"Line from ({x1}, {y1}) to ({x2}, {y2})")
    return lines

def find_intersections(image, lines):
    if lines is None:
        return image, []

    intersection_points = []
    
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            slope1 = calculate_slope(lines[i][0])
            slope2 = calculate_slope(lines[j][0])
            
            if is_near_90_degrees(slope1, slope2):
                intersection = find_intersection(lines[i][0], lines[j][0])
                if intersection:
                    intersection_points.append(intersection)
                    cv2.circle(image, intersection, radius=5, color=(255, 0, 0), thickness=-1)
                else:
                    print("intersection not found")

    return image, intersection_points


def newSlopes(line):
    x1, y1, x2, y2 = line
    if x2 - x1 == 0:
        return float('inf')
    return (y2 - y1) / (x2 - x1)

def newfind_intersection(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    # Line 1 represented as a1x + b1y = c1
    a1 = y2 - y1
    b1 = x1 - x2
    c1 = a1 * x1 + b1 * y1

    # Line 2 represented as a2x + b2y = c2
    a2 = y4 - y3
    b2 = x3 - x4
    c2 = a2 * x3 + b2 * y3

    determinant = a1 * b2 - a2 * b1

    if determinant == 0:
        # The lines are parallel
        return None
    else:
        x = (b2 * c1 - b1 * c2) / determinant
        y = (a1 * c2 - a2 * c1) / determinant

        # Check if the intersection point (x, y) lies on both line segments
        if (min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2) and
                min(x3, x4) <= x <= max(x3, x4) and min(y3, y4) <= y <= max(y3, y4)):
            return int(x), int(y)
        else:
            return None
        
def calculate_angle(slope1, slope2):
    if slope1 == float('inf'):
        angle = 90 if slope2 == 0 else math.degrees(math.atan(abs(slope2)))
    elif slope2 == float('inf'):
        angle = 90 if slope1 == 0 else math.degrees(math.atan(abs(slope1)))
    else:
        tan_angle = abs((slope2 - slope1) / (1 + slope1 * slope2))
        angle = math.degrees(math.atan(tan_angle))
    return angle

def newfind_intersections(image, lines, min_angle=80, max_angle=100):
    if lines is None:
        return image, []

    intersection_points = []

    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            slope1 = calculate_slope(lines[i][0])
            slope2 = calculate_slope(lines[j][0])
            
            angle = calculate_angle(slope1, slope2)
            if min_angle <= angle <= max_angle:
                intersection = find_intersection(lines[i][0], lines[j][0])
                if intersection:
                    intersection_points.append(intersection)
                    cv2.circle(image, intersection, radius=5, color=(255, 0, 0), thickness=-1)

    return image, intersection_points


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
cap = cv2.VideoCapture(CAM_INDEX,cv2.CAP_DSHOW)
dst_size = (1200, 1800)
ret, frame = cap.read()

output_dir = 'images/outputCalibrate'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
frame_name = 'frame_1.jpg'
frame_path = os.path.join(output_dir, frame_name)
cv2.imwrite(frame_path, frame)


lower_bound, upper_bound = load_color_presets("default")
if warp:
    red_hsv_values = read_hsv_values('hsv_presets_red.txt')
    final_points = find_corner_points_full(frame, red_hsv_values, doVerbose=True)

# Create windows
cv2.namedWindow('Lower Bounds')
cv2.namedWindow('Upper Bounds')
cv2.namedWindow('Result')
if warp:
    cv2.namedWindow('warped')
    cv2.resizeWindow('warped', 1200, 1800)
if edges:
    cv2.namedWindow('edges para')
    cv2.namedWindow('edges')


# Color presets and current color
colors = {
    'green': {'LowerH': 35, 'LowerS': 100, 'LowerV': 100, 'UpperH': 85, 'UpperS': 255, 'UpperV': 255},
    'red': {'LowerH': 0, 'LowerS': 100, 'LowerV': 100, 'UpperH': 10, 'UpperS': 255, 'UpperV': 255},
    'orange': {'LowerH': 10, 'LowerS': 100, 'LowerV': 100, 'UpperH': 25, 'UpperS': 255, 'UpperV': 255},
    'white': {'LowerH': 0, 'LowerS': 0, 'LowerV': 200, 'UpperH': 179, 'UpperS': 30, 'UpperV': 255},
    'yellow': {'LowerH': 25, 'LowerS': 100, 'LowerV': 100, 'UpperH': 35, 'UpperS': 255, 'UpperV': 255}
}
current_color = 'green'

# Toggle for circles and lines
show_circles = False
show_lines = False
show_intesections = False


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
    
    if warp:
        gen_warped_frame = warp_perspective(res, final_points, dst_size)

    if edges:
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        edgesim = cv2.Canny(gray, 50, 200, apertureSize=3)
        cv2.imshow('edges', edgesim)

    # Display lines
    if show_lines:
        linestest = find_lines(res)

    if show_intesections:
        find_intersections(res, linestest)
    # newfind_intersections(res, linestest)
    
    # Detect and count balls
    circles = detect_balls(res)
    ball_count = len(circles)
    if warp:
        circles2 = detect_balls(gen_warped_frame,min_radius=60, max_radius=65)
        ball_count2 = len(circles2)
        circles3 = detect_balls(gen_warped_frame)
        ball_count3 = len(circles3)
        circles4 = detect_balls(gen_warped_frame, min_radius=45, max_radius=50)
        ball_count4 = len(circles2)

    
    # Display circles
    if circles is not None and show_circles:
        for (x, y, r) in circles:
            cv2.circle(res, (x, y), r, (255, 255, 0), 4)
    # Display circles
    if warp:
        if circles2 is not None and show_circles:
            for (x, y, r) in circles2:
                cv2.circle(gen_warped_frame, (x, y), r, (255, 255, 0), 4)
        if circles3 is not None and show_circles:
            for (x, y, r) in circles3:
                cv2.circle(gen_warped_frame, (x, y), r, (255, 0, 0), 4)
        if circles4 is not None and show_circles:
            for (x, y, r) in circles4:
                cv2.circle(gen_warped_frame, (x, y), r, (0, 0, 255), 4)
    
    cv2.putText(res, f"Balls detected: {ball_count}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    if warp:
        cv2.putText(gen_warped_frame, f"Balls detected: {ball_count2}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Result', res)
    if warp:
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
    elif key == ord('i'): # Toggle intersections
        show_intesections = not show_intesections
    elif key in [ord('g'), ord('r'), ord('o'), ord('w'), ord('y')]:  # Preset selection keys
        preset_keys = {'g': 'green', 'r': 'red', 'o': 'orange', 'w': 'white', 'y': 'yellow'}
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

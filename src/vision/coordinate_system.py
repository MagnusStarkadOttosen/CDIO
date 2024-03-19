import cv2
import numpy as np

def find_corners(masked_image):
    corners = cv2.goodFeaturesToTrack(cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY), 4, 0.01, 10)
    corners = np.int0(corners)
    return corners

def map_to_coordinate_system(image, point, origin, scale):
    # Convert a point from image coordinates to your defined coordinate system
    x, y = point
    origin_x, origin_y = origin
    mapped_x = (x - origin_x) * scale
    mapped_y = (y - origin_y) * scale
    return mapped_x, mapped_y

def warp_perspective(image, src_points, dst_size):
    height, width = dst_size
    
    pts_dst = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype="float32")
    
    M = cv2.getPerspectiveTransform(src_points, pts_dst)
    
    warped_image = cv2.warpPerspective(image, M, (width, height))
    
    return warped_image

def draw_grid(image, real_world_size, grid_spacing_cm):
    height, width = image.shape[:2]

    scale_x = width / real_world_size[1]
    scale_y = height / real_world_size[0]
    
    num_x_lines = int(real_world_size[1] / grid_spacing_cm)
    num_y_lines = int(real_world_size[0] / grid_spacing_cm)
    
    image_with_grid = image.copy()

    for i in range(num_x_lines + 1):
        x = int(i * grid_spacing_cm * scale_x)
        cv2.line(image_with_grid, (x, 0), (x, height), (255, 255, 0), 2)

    for i in range(num_y_lines + 1):
        y = int(i * grid_spacing_cm * scale_y)
        cv2.line(image_with_grid, (0, y), (width, y), (255, 255, 0), 2)

    return image_with_grid

def detect_red(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    red_image = cv2.bitwise_and(image, image, mask=mask)
        
    return red_image



def sharpen_image(image):
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])

    sharpened_image = cv2.filter2D(image, -1, kernel)
    return sharpened_image

def clean_image(image):

    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=2)
    
    dilated = cv2.dilate(opening, kernel, iterations=2)
    
    blurred = cv2.GaussianBlur(dilated, (5,5), 0)
    
    return blurred


def erode_image(image, i=1):
    kernel = np.ones((4, 4), np.uint8) 
    img_erosion = cv2.erode(image, kernel, iterations=i) 
    
    return img_erosion

def find_line_intersections(image):
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=150)
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            print(f"Line from ({x1}, {y1}) to ({x2}, {y2})")
            

    return image, lines

def calculate_slope(line):
    x1, y1, x2, y2 = line
    if x2 == x1:
        return np.inf  
    return (y2 - y1) / (x2 - x1)

def find_intersection(l1, l2):
    x1, y1, x2, y2 = l1
    x3, y3, x4, y4 = l2
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0:
        return None 
    px = ((x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2) * (x3*y4 - y3*x4)) / den
    py = ((x1*y2 - y1*x2) * (y3 - y4) - (y1 - y2) * (x3*y4 - y3*x4)) / den
    return int(px), int(py)

def is_near_90_degrees(slope1, slope2, tolerance=5):
    if slope1 == np.inf and slope2 == 0:
        return True
    if slope2 == np.inf and slope1 == 0:
        return True
    if slope1 == np.inf or slope2 == np.inf:
        return False
    angle = np.abs(np.arctan((slope2 - slope1) / (1 + slope1 * slope2)))
    angle_deg = np.degrees(angle)
    return 85 <= angle_deg <= 95

def distance_between_points(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
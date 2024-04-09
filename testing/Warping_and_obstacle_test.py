import cv2

from src.client.field.coordinate_system import *
from src.client.vision.filters import *

#Desired output size (dimensions in pixels for the warped image)
dst_size = (1200, 1800)  # width, height

# Path from where images comes from and path where the processed images are stored
input_folder_path = 'images/'
output_folder_path = 'images/outputObstacle/'

# Name of the image to be used
image_name = 'Course_X2.jpg'
input_image_path = input_folder_path + image_name
image = cv2.imread(input_image_path)

if image is not None:
    #Filter for red wall
    red_image = temp_filter_for_red_wall(image)
    red_image_name = 'red_' + image_name
    red_image_path = output_folder_path + red_image_name
    cv2.imwrite(red_image_path, red_image)
    
    clean_image = clean_image(red_image)
    clean_image_name = 'clean_' + image_name
    clean_image_path = output_folder_path + clean_image_name
    cv2.imwrite(clean_image_path, clean_image)
    
    edge_image, lines = find_lines(clean_image)
    edge_image_name = 'edge_' + image_name
    edge_image_path = output_folder_path + edge_image_name
    cv2.imwrite(edge_image_path, edge_image)
    
    lines = np.array(lines)
    lines = lines.reshape(-1, 4)
    
    intersection_points = []
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            slope1 = calculate_slope(lines[i])
            slope2 = calculate_slope(lines[j])
            if is_near_90_degrees(slope1, slope2):
                intersection = find_intersection(lines[i], lines[j])
                if intersection:
                    intersection_points.append(intersection)
                    print(f"Intersection point: {intersection}") 
                    cv2.circle(clean_image, intersection, radius=5, color=(255, 0, 0), thickness=-1) 
    
    height, width, _ = image.shape
    center_x, center_y = width // 2, height // 2
    
    quadrants = {1: [], 2: [], 3: [], 4: []}

    # Categorize points into quadrants
    for point in intersection_points:
        x, y = point
        if x > center_x and y < center_y:
            quadrants[1].append(point)  # Quadrant I
        elif x < center_x and y < center_y:
            quadrants[2].append(point)  # Quadrant II
        elif x < center_x and y > center_y:
            quadrants[3].append(point)  # Quadrant III
        elif x > center_x and y > center_y:
            quadrants[4].append(point)  # Quadrant IV
    
    # Find the closest point to the center in each quadrant
    closest_points = []
    for q in [2, 1, 4, 3]:
        if quadrants[q]:  # Check if the list is not empty
            # closest_point = min(quadrants[q], key=lambda point: distance_between_points(point, (center_x, center_y)))
            closest_point = min(quadrants[q], key=lambda point: np.sqrt((point[0]-center_x) ** 2 + (point[1]-center_y) ** 2))
            closest_points.append(closest_point)
    
    final_points = np.array(closest_points, dtype="float32")
    
    gen_warped_image = warp_perspective(image, final_points, dst_size)
    
    gen_warped_image_name = 'gen_warped_' + image_name
    gen_warped_image_path = output_folder_path + gen_warped_image_name
    cv2.imwrite(gen_warped_image_path, gen_warped_image)
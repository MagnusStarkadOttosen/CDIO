import cv2

from src.client.field.coordinate_system import *
from src.client.vision.filters import *
from src.client.vision.shape_detection import detect_balls

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
    
    corners = find_corner_points_full(image, doVerbose=True)
    
    gen_warped_image = warp_perspective(image, corners, dst_size)
    
    gen_warped_image_name = 'gen_warped2_' + image_name
    gen_warped_image_path = output_folder_path + gen_warped_image_name
    cv2.imwrite(gen_warped_image_path, gen_warped_image)
    
    # Filter to only show the red walls from the original image.
    red_image = temp_filter_for_red_wall(gen_warped_image)
    clean_image = clean_the_image(red_image)
    
    edge_image, lines = find_lines(clean_image, resolution=5, doVerbose=True)
    red_image_name = 'red2_' + image_name
    red_image_path = output_folder_path + red_image_name
    cv2.imwrite(red_image_path, edge_image)
    
    print("test")
    
    # edge_image2 = cluster_lines_into_4(gen_warped_image, lines)
    edge_image2 = cluster_lines(gen_warped_image, lines)

    red_image_name = 'red3_' + image_name
    red_image_path = output_folder_path + red_image_name
    cv2.imwrite(red_image_path, edge_image2)

    white_image = filter_image_white(gen_warped_image)
    white_image_name = 'white_' + image_name
    white_image_path = output_folder_path + white_image_name
    cv2.imwrite(white_image_path, white_image)

    balls = detect_balls(white_image)

    
    
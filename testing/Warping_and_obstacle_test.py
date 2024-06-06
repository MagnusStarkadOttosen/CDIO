import cv2

from src.client.field.coordinate_system import *
from src.client.vision.filters import *
from src.client.vision.shape_detection import detect_egg


#Desired output size (dimensions in pixels for the warped image)
dst_size = (1200, 1800)  # width, height

# Path from where images comes from and path where the processed images are stored
input_folder_path = 'originalImages/'
output_folder_path = 'originalImages/'

# Name of the image to be used
image_name = 'newCourse.jpg'
input_image_path = input_folder_path + image_name
image = cv2.imread(input_image_path)


def print_image(image, balls, image_name):
    if balls is not None:
        idx = 0
        for ball in balls:
            # print(f"{type(ball[0])},type({ball[1]}),type({ball[2]})")
            # Draw the outer circle
            cv2.circle(image, (ball[0], ball[1]), ball[2], (128, 0, 128), 2)
            # Draw the center of the circle
            cv2.circle(image, (ball[0], ball[1]), 2, (128, 0, 128), 3)
            # Enumerate the detected balls
            cv2.putText(image, str(idx), (ball[0], ball[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            idx += 1
            print("ball x:", ball[0], "y:", ball[1])

        write_image_to_file('circles_detected_' + image_name, image)
    else:
        print("No balls detected to draw on the image.")

def write_image_to_file(output_image_name, output_img):
    output_image_name = 'processed_' + output_image_name
    output_image_path = output_folder_path + output_image_name
    print("output_image_path: ", output_image_path, "output_image_name: ", output_image_name)
    cv2.imwrite(output_image_path, output_img)
    print(f"Processed image saved at: {output_image_path}")
if image is not None:
    
    corners = find_corner_points_full(image, doVerbose=True)
    
    gen_warped_image = warp_perspective(image, corners, dst_size)


    green_image = filter_image_green(gen_warped_image)
    green_image_name = 'green2_' + image_name
    green_image_path = output_folder_path + green_image_name
    cv2.imwrite(green_image_path, green_image)

    balls_image_name = 'ballTestTrial5' + image_name
    balls_image_path = output_folder_path + balls_image_name
    balls= detect_egg(gen_warped_image)
    print_image(gen_warped_image,balls,balls_image_name)
    #cv2.imwrite(balls_image_pathb, green_image)






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
    # edge_image2 = cluster_lines(gen_warped_image, lines)

    # red_image_name = 'red3_' + image_name
    # red_image_path = output_folder_path + red_image_name
    # cv2.imwrite(red_image_path, edge_image2)

    white_image = filter_image_white(gen_warped_image)
    white_image_name = 'white_' + image_name
    white_image_path = output_folder_path + white_image_name
    cv2.imwrite(white_image_path, white_image)

    balls = detect_balls(green_image)

    
    
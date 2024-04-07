import cv2

from src.client.vision.detector_robot import detect_ball
from src.client.vision.filters import filter_image_red, filter_image_green

# Path from where images comes from and path where the processed images are stored
input_folder_path = 'images/'
output_folder_path = 'images/'

# Name of the image to be used
image_name = ('1.jpg', 'image_with_robot.jpeg')


def test_filter_image_red():
    image = cv2.imread(input_folder_path + image_name[1])
    filtered_image = filter_image_red(image)
    write_image_to_file('filter_red_' + image_name[1], filtered_image)


def test_detect_balls():
    image = cv2.imread(input_folder_path + image_name[0])
    if image is not None:

        circles = detect_ball(image)

        # shape_detector.detect_ball()

        # shape_detector.detect_walls()

        # shape_detector.draw_corners_debug(image)
        # shape_detector.draw_coordinate_system(image)

        write_image_to_file('detect_balls_' + image_name[0], image)

    else:
        print("Error: Image not found. Please check the input folder path and image name.")


def write_image_to_file(output_image_name, output_img):
    output_image_name = 'processed_' + output_image_name
    output_image_path = output_folder_path + output_image_name
    print("output_image_path: ", output_image_path, "output_image_name: ", output_image_name)
    cv2.imwrite(output_image_path, output_img)
    print(f"Processed image saved at: {output_image_path}")


test_filter_image_red()
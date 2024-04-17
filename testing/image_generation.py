import cv2
import unittest

from src.client.vision.filters import (filter_image_red, filter_image_green,
                                       apply_gray, apply_canny, filter_image_white)

# Path from where images comes from and path where the processed images are stored
input_folder_path = 'images/'
output_folder_path = 'images/'

# Name of the image to be used
image_name = ('1.jpg', 'image_with_robot.jpeg', 'robot_ball_90.jpeg',
              'gen_warped2_newCourse_brightened.jpg', '9_balls_on_field.jpeg',
              'gen_warped2_newCourse.jpg', 'gen_warped2_newCourse_purple_robot.jpg',
              'gen_warped2_newCourse_darkened.jpg')


class TestColorFilters(unittest.TestCase):
    def test_filter_image_red(self):
        name = image_name[2]
        image = cv2.imread(input_folder_path + name)
        filtered_image = filter_image_red(image)
        write_image_to_file('filter_red_' + name, filtered_image)

    def test_filter_image_green(self):
        image = cv2.imread(input_folder_path + image_name[1])
        filtered_image = filter_image_green(image)
        write_image_to_file('filter_green_' + image_name[1], filtered_image)

    def test_filter_image_white(self):
        image = cv2.imread(input_folder_path + image_name[7])
        filtered_image = filter_image_white(image)
        write_image_to_file('filter_white_' + image_name[7], filtered_image)

    def test_grayed_filter_image_red(self):
        image = cv2.imread(input_folder_path + image_name[1])
        red_img = filter_image_red(image)
        gray = apply_gray(red_img)
        write_image_to_file('gray_' + image_name[1], gray)

    def test_canny_filter_gray(self):
        image = cv2.imread(input_folder_path + 'robot_with_circles.jpg')
        red_img = filter_image_red(image)
        gray = apply_gray(red_img)
        edges = cv2.Canny(gray, 100, 200)
        write_image_to_file('edges_' + 'robot_with_circles.jpg', edges)

    def test_canny_filter_three_balls(self):
        image = cv2.imread(input_folder_path + image_name[0])
        gray = apply_gray(image)
        edges = apply_canny(gray)
        write_image_to_file('edges_colour_' + image_name[1], edges)


if __name__ == '__main__':
    unittest.main()


def write_image_to_file(output_image_name, output_img):
    output_image_name = 'processed_' + output_image_name
    output_image_path = output_folder_path + output_image_name
    print("output_image_path: ", output_image_path, "output_image_name: ", output_image_name)
    cv2.imwrite(output_image_path, output_img)
    print(f"Processed image saved at: {output_image_path}")
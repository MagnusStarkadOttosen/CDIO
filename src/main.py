from camera.filters import filter_image
from camera.filters import save_image
#Path from where images comes from and path where the processed images are stored
input_folder_path = 'images/'
output_folder_path = 'images/'

#Name of the image to be used
image_name = 'bowl.jpg'

input_image_path = input_folder_path + image_name

image = filter_image(input_image_path)
save_image('bowl.JPG', output_folder_path, image)
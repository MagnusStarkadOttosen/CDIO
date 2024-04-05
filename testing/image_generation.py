import cv2

#Path from where images comes from and path where the processed images are stored
input_folder_path = 'images/'
output_folder_path = 'images/'

#Name of the image to be used
image_name = 'detectballs.jpg'
input_image_path = input_folder_path + image_name
image = cv2.imread(input_image_path)



if image is not None:

  circles = detect_ball(image)



  # shape_detector.detect_ball()
  #shape_detector.detect_walls()

  # shape_detector.draw_corners_debug(image)
  # shape_detector.draw_coordinate_system(image)

  output_image_name = 'processed_' + image_name
  output_image_path = output_folder_path + output_image_name

  output_image_name_red = "Processed_img_red" + image_name
  output_image_path_red = output_folder_path + output_image_name_red

  cv2.imwrite(output_image_path, image)
  print(f"Processed image saved at: {output_image_path}")

else:
  print("Error: Image not found. Please check the input folder path and image name.")


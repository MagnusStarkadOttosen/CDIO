import cv2
import numpy as np

from src.vision.shape_detection import Shapes
from testing.visualization import draw_shapes
from src.vision.coordinate_system import *
from src.vision.filters import *
from sklearn.cluster import KMeans

#Manually placed corners on original image
#corners = np.array([[417, 73], [1650, 66], [1689, 987], [403, 985]], dtype="float32") #Top left, top right, buttom right, buttom left
corners = np.array([[393, 49], [1678, 42], [1723, 1005], [378, 1000]], dtype="float32")

#Real world dimensions in cm
real_world_size = (120, 180)  # height, width

#Desired output size (dimensions in pixels for the warped image)
dst_size = (1200, 1800)  # width, height

#Path from where images comes from and path where the processed images are stored
input_folder_path = 'images/'
output_folder_path = 'images/'

#Name of the image to be used
image_name = 'full_course1.jpg'
input_image_path = input_folder_path + image_name
image = cv2.imread(input_image_path)




if image is not None:
    
    warped_image = warp_perspective(image, corners, dst_size)
    
    warped_image_name = 'warped_' + image_name
    warped_image_path = output_folder_path + warped_image_name
    cv2.imwrite(warped_image_path, warped_image)

    grid_image = draw_grid(warped_image, real_world_size, grid_spacing_cm=10)

    grid_image_name = 'grid_' + image_name
    grid_image_path = output_folder_path + grid_image_name
    cv2.imwrite(grid_image_path, grid_image)
    
    red_image = detect_red(image)
    
    red_image_name = 'red_' + image_name
    red_image_path = output_folder_path + red_image_name
    cv2.imwrite(red_image_path, red_image)

    sharp_image = sharpen_image(red_image)

    sharp_image_name = 'sharp_' + image_name
    sharp_image_path = output_folder_path + sharp_image_name
    cv2.imwrite(sharp_image_path, sharp_image)
    
    clean_image = clean_image(red_image)
    
    # clean_image = erode_image(clean_image, 4)
    
    edge_image, lines = find_line_intersections(clean_image)
    
    arr = np.array(lines)
    
    print(arr.shape)
    arr = arr.reshape(-1, 4)
    print(arr.shape)
    kmeans = KMeans(n_clusters=4, random_state=0).fit(arr)
    centroids = kmeans.cluster_centers_
    sorted_centroids = sorted(centroids, key=lambda x: (x[0], x[1]))
    for i, centroid in enumerate(sorted_centroids, start=1):
        print(f"Centroid {i}: (x={centroid[0]}, y={centroid[1]})")
        cv2.circle(edge_image, (int(centroid[0]), int(centroid[1])), radius=5, color=(255, 0, 0), thickness=-1)

    
    
    clean_image_name = 'clean_' + image_name
    clean_image_path = output_folder_path + clean_image_name
    cv2.imwrite(clean_image_path, clean_image)
    

        

    edge_image_name = 'edge_' + image_name
    edge_image_path = output_folder_path + edge_image_name
    cv2.imwrite(edge_image_path, edge_image)
    

    print(f"Processed image done!") 
else:
    print("Error: Image not found. Please check the input folder path and image name.")


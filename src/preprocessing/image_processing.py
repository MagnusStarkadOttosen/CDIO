import cv2
import numpy as np
import os

# path to the image
image_path = "/Users/lynguyenhansen/Documents/GitHub/CDIO/originalImages/Image 4.jpeg"

# read the image
image = cv2.imread(image_path)

# convert the image to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# define the range of white color in HSV
white_lower = np.array([0, 0, 200])
white_upper = np.array([180, 30, 255])
orange_lower = np.array([5, 150, 150])
orange_upper = np.array([15, 255, 255])

# Create a window to adjust the HSV range
cv2.namedWindow('Adjust HSV')

def nothing(x):
    pass

# Create trackbars for lower and upper HSV values
cv2.createTrackbar('Lower H', 'Adjust HSV', orange_lower[0], 180, nothing)
cv2.createTrackbar('Lower S', 'Adjust HSV', orange_lower[1], 255, nothing)
cv2.createTrackbar('Lower V', 'Adjust HSV', orange_lower[2], 255, nothing)
cv2.createTrackbar('Upper H', 'Adjust HSV', orange_upper[0], 180, nothing)
cv2.createTrackbar('Upper S', 'Adjust HSV', orange_upper[1], 255, nothing)
cv2.createTrackbar('Upper V', 'Adjust HSV', orange_upper[2], 255, nothing)

cv2.createTrackbar('Lower H', 'Adjust HSV', white_lower[0], 180, nothing)
cv2.createTrackbar('Lower S', 'Adjust HSV', white_lower[1], 255, nothing)
cv2.createTrackbar('Lower V', 'Adjust HSV', white_lower[2], 255, nothing)
cv2.createTrackbar('Upper H', 'Adjust HSV', white_upper[0], 180, nothing)
cv2.createTrackbar('Upper S', 'Adjust HSV', white_upper[1], 255, nothing)
cv2.createTrackbar('Upper V', 'Adjust HSV', white_upper[2], 255, nothing)

while True:
    # Get the current positions of the trackbars for orange
    orange_lower_h = cv2.getTrackbarPos('Orange Lower H', 'Adjust HSV')
    orange_lower_s = cv2.getTrackbarPos('Orange Lower S', 'Adjust HSV')
    orange_lower_v = cv2.getTrackbarPos('Orange Lower V', 'Adjust HSV')
    orange_upper_h = cv2.getTrackbarPos('Orange Upper H', 'Adjust HSV')
    orange_upper_s = cv2.getTrackbarPos('Orange Upper S', 'Adjust HSV')
    orange_upper_v = cv2.getTrackbarPos('Orange Upper V', 'Adjust HSV')

    # Get the current positions of the trackbars for white
    white_lower_h = cv2.getTrackbarPos('White Lower H', 'Adjust HSV')
    white_lower_s = cv2.getTrackbarPos('White Lower S', 'Adjust HSV')
    white_lower_v = cv2.getTrackbarPos('White Lower V', 'Adjust HSV')
    white_upper_h = cv2.getTrackbarPos('White Upper H', 'Adjust HSV')
    white_upper_s = cv2.getTrackbarPos('White Upper S', 'Adjust HSV')
    white_upper_v = cv2.getTrackbarPos('White Upper V', 'Adjust HSV')

    # Update the HSV range for orange
    orange_lower = np.array([orange_lower_h, orange_lower_s, orange_lower_v])
    orange_upper = np.array([orange_upper_h, orange_upper_s, orange_upper_v])

    # Update the HSV range for white
    white_lower = np.array([white_lower_h, white_lower_s, white_lower_v])
    white_upper = np.array([white_upper_h, white_upper_s, white_upper_v])


    # create a mask for the white color
    white_mask = cv2.inRange(hsv, white_lower, white_upper)
    orange_mask = cv2.inRange(hsv, orange_lower, orange_upper)

    # find contours in the mask
    white_contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    orange_contours, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   # Draw the contours on the original image for visualization
    output_image = image.copy()
    cv2.drawContours(output_image, orange_contours, -1, (0, 255, 0), 2)
    cv2.drawContours(output_image, white_contours, -1, (255, 0, 0), 2)

    # Display the result
    cv2.imshow('Adjust HSV', output_image)


    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()

# create a directory to save the extracted images
output_dir = 'extracted_images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# function to save the contours as images
def save_contours(contours, color_name, min_area=70, max_area=5000):
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            if 0.8 < aspect_ratio < 1.2:  # filter out non-circular objects
                roi = image[y:y+h, x:x+w]
                output_path = os.path.join(output_dir, f"{color_name}_{i}.png")
                cv2.imwrite(output_path, roi)

# save the extracted images
save_contours(white_contours, 'white_ball')
save_contours(orange_contours, 'orange_ball')

print("Extracted and saved objects from the original image")

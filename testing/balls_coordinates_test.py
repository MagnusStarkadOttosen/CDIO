import cv2

from src.client.vision.shape_detection import detect_balls
from testing.visualization import draw_circles

image_path = 'images/5.jpg'
image = cv2.imread(image_path)

if image is None:
    print(f"Error: Unable to read image from path {image_path}")
else:
    print("Image successfully loaded.")

    # Detect balls
    circles = detect_balls(image)

    # Draw detected circles
    draw_circles(circles, image)

    # Save the result to a file instead of displaying it
    output_image_path = 'images/output_detected_circles.jpg'
    cv2.imwrite(output_image_path, image)
    print(f"Output image saved to {output_image_path}")
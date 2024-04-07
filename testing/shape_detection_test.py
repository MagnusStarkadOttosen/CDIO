import cv2

from src.client.vision.shape_detection import detect_balls
from testing.image_generation import write_image_to_file

image_name = "9_balls_on_field.jpeg"

image = cv2.imread('images/'+image_name)

balls = detect_balls(image)

for ball in balls:
    # Draw the outer circle
    cv2.circle(image, (ball[0], ball[1]), ball[2], (128, 0, 128), 2)
    # Draw the center of the circle
    cv2.circle(image, (ball[0], ball[1]), 2, (128, 0, 128), 3)
    # Enumerate the detected balls
    # cv2.putText(image, str(idx + 1), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    print(f"ball x: {ball[0]}, y: {ball[1]}")

write_image_to_file('circles_detected_' + image_name, image)

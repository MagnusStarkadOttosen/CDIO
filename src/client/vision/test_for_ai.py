import cv2
import time

from src.client.vision.AIBallDetection import detect_balls_with_model

# Load the image
image_path = "originalImages/PreWarpedCourse.jpg"
image = cv2.imread(image_path)

start_time = time.time()
  
# Detect balls
white_balls, orange_balls = detect_balls_with_model(image)

end_time = time.time()
elapsed_time = end_time - start_time

# Print the results
print("White balls:", white_balls)
print("Orange balls:", orange_balls)
print(f"Time taken for ball detection: {elapsed_time:.2f} seconds")

# Draw bounding boxes on the image
for ball in white_balls:
    x, y, r = ball
    # Draw the circle
    cv2.circle(image, (x, y), r, (0, 255, 0), 2)
    # Put the label near the circle
    label = f"white_ball: radius={r}"
    cv2.putText(image, label, (x - r, y - r - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
for ball in orange_balls:
    x, y, r = ball
    # Draw the circle
    cv2.circle(image, (x, y), r, (0, 0, 255), 2)
    # Put the label near the circle
    label = f"orange_ball: radius={r}"
    cv2.putText(image, label, (x - r, y - r - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# Save or display the image
cv2.imwrite("result.jpg", image)
cv2.imshow("Result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

import os
import cv2
import warnings
from dotenv import load_dotenv
import inference

# Suppress specific warnings
warnings.filterwarnings("ignore", message="Specified provider 'CUDAExecutionProvider'")
warnings.filterwarnings("ignore", message="Specified provider 'OpenVINOExecutionProvider'")

# Load environment variables from .env file
load_dotenv()

# Load the model
model = inference.get_model("detect-balls/3")

# Path to your input image
image_path = "originalImages/PreWarpedCourse.jpg"

# Run inference on the image
results_list = model.infer(image=image_path)

# Load the image with OpenCV
image = cv2.imread(image_path)

# Iterate over the list of results
for results in results_list:
    # Draw bounding boxes on the image
    for prediction in results.predictions:
        x1 = int(prediction.x - prediction.width / 2)
        y1 = int(prediction.y - prediction.height / 2)
        x2 = int(prediction.x + prediction.width / 2)
        y2 = int(prediction.y + prediction.height / 2)

        # Draw the bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Put the label near the bounding box
        label = f"{prediction.class_name}: {prediction.confidence:.2f}"
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Save or display the image
cv2.imwrite("result.jpg", image)
# cv2.imshow("Result", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Print the results
print(results_list)

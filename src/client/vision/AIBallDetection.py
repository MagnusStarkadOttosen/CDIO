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

# Load the model once, so it doesn't reload every time the function is called
model = inference.get_model("detect-balls/3")

def detect_balls_with_model(image, min_confidence=0.5):
    # Convert the image to a format suitable for the model
    temp_image_path = "temp_image.jpg"
    cv2.imwrite(temp_image_path, image)
    
    # Run inference on the image
    results_list = model.infer(image=temp_image_path)
    
    # List to store detected balls
    detected_balls = []

    # Iterate over the list of results and collect detections
    for results in results_list:
        for prediction in results.predictions:
            if prediction.confidence >= min_confidence:
                ball_data = {
                    'x': prediction.x,
                    'y': prediction.y,
                    'width': prediction.width,
                    'height': prediction.height,
                    'confidence': prediction.confidence,
                    'class_name': prediction.class_name,
                }
                detected_balls.append(ball_data)
    
    return detected_balls

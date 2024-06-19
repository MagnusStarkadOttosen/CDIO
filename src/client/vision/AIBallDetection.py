import os
import cv2
import warnings
from dotenv import load_dotenv
import inference
import numpy as np

# Suppress specific warnings
warnings.filterwarnings("ignore", message="Specified provider 'CUDAExecutionProvider'")
warnings.filterwarnings("ignore", message="Specified provider 'OpenVINOExecutionProvider'")

# Load environment variables from .env file
load_dotenv()

# Load the model once, so it doesn't reload every time the function is called
model = inference.get_model("detect-balls/5")

def detect_balls_with_model(image, min_confidence=0.5):
    
    results_list = model.infer(image=image)
    
    # Lists to store detected balls
    white_balls = []
    orange_balls = []

    # Iterate over the list of results and collect detections
    for results in results_list:
        for prediction in results.predictions:
            if prediction.confidence >= min_confidence:
                ball_data = [int(prediction.x), int(prediction.y), 5]  # Set radius to 5
                if prediction.class_name == 'white_ball':
                    white_balls.append(ball_data)
                elif prediction.class_name == 'orange_ball':
                    orange_balls.append(ball_data)
    
    return np.array(white_balls, dtype=int), np.array(orange_balls, dtype=int)

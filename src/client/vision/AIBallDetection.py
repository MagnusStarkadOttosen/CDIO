import os
import cv2
import warnings
from dotenv import load_dotenv
import inference
import numpy as np

from src.client.utilities import log_balls

# Suppress specific warnings
warnings.filterwarnings("ignore", message="Specified provider 'CUDAExecutionProvider'")
warnings.filterwarnings("ignore", message="Specified provider 'OpenVINOExecutionProvider'")

# Load environment variables from .env file
load_dotenv()

# Load the model once, so it doesn't reload every time the function is called
model = inference.get_model("detect-balls/6")

def detect_balls_with_model(image, min_confidence=0.5):
    """
    Detects white and orange balls in the given image using a pre-trained model.

    Parameters
    ----------
    image : numpy.ndarray
        The input image in which to detect balls.
    min_confidence : float, optional
        The minimum confidence threshold for detections, default is 0.5.

    Returns
    -------
    tuple
        Two numpy arrays containing the detected white balls and orange balls respectively.
    """
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
    log_balls(white_balls)
    log_balls(len(white_balls))
    log_balls(orange_balls)
    return np.array(white_balls, dtype=int), np.array(orange_balls, dtype=int)

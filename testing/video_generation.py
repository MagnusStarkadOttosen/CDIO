import cv2
import numpy as np

from src.vision.shape_detection import Shapes
from testing.visualization import draw_shapes

input_folder_path = "video/"
output_folder_path = "video/"

video_name = "vid1.MOV"
input_video_path = input_folder_path + video_name
video = cv2.VideoCapture(input_video_path)

if not video.isOpened():
    print("Error: Could not open video.")
    exit()

fps = video.get(cv2.CAP_PROP_FPS)
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
output_video_path = output_folder_path + "output.mov"
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

while True:
    ret, frame = video.read()
    if not ret: #If no next frame break
        break

    shape_detector = Shapes(frame)
    shape_detector.detect_balls()

    draw_shapes(shape_detector.circles, shape_detector.lines, frame)

    out.write(frame)

video.release()
out.release()
print(f"Processed video saved at: {output_video_path}")
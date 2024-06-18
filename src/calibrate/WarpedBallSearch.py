import os
import sys
import cv2
import numpy as np

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.calibrate.save_and_load_HSV import load_color_presets, save_color_presets
from src.client.field.coordinate_system import find_corner_points_full, warp_perspective
from src.client.hsvLoad import read_hsv_values
from src.client.vision.shape_detection import detect_balls


def nothing(x):
    pass

def main():
    CAM_INDEX = 2
    cap = cv2.VideoCapture(CAM_INDEX, cv2.CAP_DSHOW)

    # Create windows
    cv2.namedWindow('HSV Thresholds', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('HSV Thresholds', 600, 400)
    cv2.namedWindow('Result')

    dst_size = (1200, 1800)
    ret, frame = cap.read()

    # Save a snapshot before warping
    output_dir = 'images/outputCalibrate'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    frame_name = 'frame_not_warped.jpg'
    frame_path = os.path.join(output_dir, frame_name)
    cv2.imwrite(frame_path, frame)

    current_color = 'default'
    lower_bound, upper_bound = load_color_presets("default")

    red_hsv_values = read_hsv_values('hsv_presets_red.txt')
    final_points = find_corner_points_full(frame, red_hsv_values, doVerbose=True)

    cv2.namedWindow('HSV Thresholds', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('HSV Thresholds', 600, 400)
    cv2.namedWindow('Result')


    # Initialize trackbars for the default color
    for k, v in zip(['LowerH', 'LowerS', 'LowerV', 'UpperH', 'UpperS', 'UpperV'], np.concatenate(load_color_presets('default'))):
        cv2.createTrackbar(k, 'HSV Thresholds', v, 179 if 'H' in k else 255, nothing)


    show_circles = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_bound = np.array([cv2.getTrackbarPos('LowerH', 'HSV Thresholds'),
                                cv2.getTrackbarPos('LowerS', 'HSV Thresholds'),
                                cv2.getTrackbarPos('LowerV', 'HSV Thresholds')])
        upper_bound = np.array([cv2.getTrackbarPos('UpperH', 'HSV Thresholds'),
                                cv2.getTrackbarPos('UpperS', 'HSV Thresholds'),
                                cv2.getTrackbarPos('UpperV', 'HSV Thresholds')])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        
        gen_warped_frame = warp_perspective(res, final_points, dst_size)
        
        if show_circles:
            # Detect and count balls
            circles_small = detect_balls(res)
            ball_count_small = len(circles_small)

            circles_pivot = detect_balls(gen_warped_frame, min_radius=60, max_radius=65)
            ball_count_pivot = len(circles_pivot)
                
            circles_direction = detect_balls(gen_warped_frame, min_radius=45, max_radius=50)
            ball_count_direction = len(circles_direction)

            # Draw the circles
            if circles_small is not None:
                for (x, y, r) in circles_small:
                    cv2.circle(gen_warped_frame, (x, y), r, (255, 255, 0), 4)
            if circles_pivot is not None:
                for (x, y, r) in circles_pivot:
                    cv2.circle(gen_warped_frame, (x, y), r, (0, 0, 255), 4)
            if circles_direction is not None:
                for (x, y, r) in circles_direction:
                    cv2.circle(gen_warped_frame, (x, y), r, (255, 0, 0), 4)
            cv2.putText(gen_warped_frame, f"Balls detected: {ball_count_small}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        

        # Show images
        cv2.imshow('warped', gen_warped_frame)

        # Keybinds
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            save_color_presets(current_color, lower_bound, upper_bound)
        elif key == ord('c'): # Toggle circles
            show_circles = not show_circles
        elif key == ord('d'):  # Switch to default
            current_color = 'default'
            lower_bound, upper_bound = load_color_presets(current_color)
        elif key == ord('w'):  # Switch to white
            current_color = 'white'
            lower_bound, upper_bound = load_color_presets(current_color)
        elif key == ord('r'):  # Switch to red
            current_color = 'red'
            lower_bound, upper_bound = load_color_presets(current_color)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
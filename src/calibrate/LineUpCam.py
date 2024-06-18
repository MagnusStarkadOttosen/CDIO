import os
import sys
import cv2
import numpy as np

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.calibrate.save_and_load_HSV import load_color_presets, save_color_presets
from src.client.field.coordinate_system import find_all_intersections, find_lines

def nothing(x):
    pass


def main():
    CAM_INDEX = 2
    cap = cv2.VideoCapture(CAM_INDEX, cv2.CAP_DSHOW)

    # Create windows
    cv2.namedWindow('HSV Thresholds', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('HSV Thresholds', 600, 400)
    cv2.namedWindow('Result')

    # Initialize trackbars for the red color
    color = 'red'
    lower_bound, upper_bound = load_color_presets(color)
    for k, v in zip(['LowerH', 'LowerS', 'LowerV', 'UpperH', 'UpperS', 'UpperV'], np.concatenate((lower_bound, upper_bound))):
        cv2.createTrackbar(k, 'HSV Thresholds', v, 179 if 'H' in k else 255, nothing)

    current_color = 'default'

    show_lines = False
    show_intersections = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        if current_color == 'red':
            lower_bound = np.array([cv2.getTrackbarPos('LowerH', 'HSV Thresholds'),
                                    cv2.getTrackbarPos('LowerS', 'HSV Thresholds'),
                                    cv2.getTrackbarPos('LowerV', 'HSV Thresholds')])
            upper_bound = np.array([cv2.getTrackbarPos('UpperH', 'HSV Thresholds'),
                                    cv2.getTrackbarPos('UpperS', 'HSV Thresholds'),
                                    cv2.getTrackbarPos('UpperV', 'HSV Thresholds')])
        else:
            lower_bound, upper_bound = load_color_presets(current_color)

        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        res = cv2.bitwise_and(frame, frame, mask=mask)

        if show_lines:
            lines = find_lines(res)
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(res, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if show_intersections:
            intersections = find_all_intersections(res, lines)
            for intersection in intersections:
                cv2.circle(res, intersection, radius=5, color=(255, 0, 0), thickness=-1) 

        cv2.imshow('Result', res)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s') and current_color == 'red':
            save_color_presets(current_color, lower_bound, upper_bound)
        elif key == ord('l'): # Toggle lines
            show_lines = not show_lines
        elif key == ord('i'): # Toggle intersections
            show_intersections = not show_intersections
        elif key in [ord('d'), ord('r')]:  # Preset selection keys
            preset_keys = {'d': 'default', 'r': 'red'}
            current_color = preset_keys[chr(key)]
            lower_bound, upper_bound = load_color_presets(current_color)
            if current_color == 'red' and lower_bound is not None and upper_bound is not None:
                cv2.setTrackbarPos('LowerH', 'HSV Thresholds', lower_bound[0])
                cv2.setTrackbarPos('LowerS', 'HSV Thresholds', lower_bound[1])
                cv2.setTrackbarPos('LowerV', 'HSV Thresholds', lower_bound[2])
                cv2.setTrackbarPos('UpperH', 'HSV Thresholds', upper_bound[0])
                cv2.setTrackbarPos('UpperS', 'HSV Thresholds', upper_bound[1])
                cv2.setTrackbarPos('UpperV', 'HSV Thresholds', upper_bound[2])

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
import cv2
import numpy as np

def nothing(x):
    pass

def save_color_presets(color, lower_bound, upper_bound, base_filename="hsv_presets"):
    filename = f"{base_filename}_{color}.txt"
    with open(filename, "w") as file:
        file.write(f"Lower HSV: {lower_bound.tolist()}\n")
        file.write(f"Upper HSV: {upper_bound.tolist()}\n")
    print(f"{color.capitalize()} HSV values saved to {filename}")

# Capture from camera
cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)

# Create windows
cv2.namedWindow('Lower Bounds')
cv2.namedWindow('Upper Bounds')
cv2.namedWindow('Result')

# Color presets and current color
colors = {
    'green': {'LowerH': 35, 'LowerS': 100, 'LowerV': 100, 'UpperH': 85, 'UpperS': 255, 'UpperV': 255},
    'red': {'LowerH': 0, 'LowerS': 100, 'LowerV': 100, 'UpperH': 10, 'UpperS': 255, 'UpperV': 255},
    'orange': {'LowerH': 10, 'LowerS': 100, 'LowerV': 100, 'UpperH': 25, 'UpperS': 255, 'UpperV': 255},
    'white': {'LowerH': 0, 'LowerS': 0, 'LowerV': 200, 'UpperH': 179, 'UpperS': 30, 'UpperV': 255}
}
current_color = 'green'

# Initialize trackbars for the initial color (green)
for k, v in colors[current_color].items():
    window = 'Lower Bounds' if 'Lower' in k else 'Upper Bounds'
    cv2.createTrackbar(k, window, v, 179 if 'H' in k else 255, nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to HSV and get trackbar positions
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([cv2.getTrackbarPos('LowerH', 'Lower Bounds'), cv2.getTrackbarPos('LowerS', 'Lower Bounds'), cv2.getTrackbarPos('LowerV', 'Lower Bounds')])
    upper_bound = np.array([cv2.getTrackbarPos('UpperH', 'Upper Bounds'), cv2.getTrackbarPos('UpperS', 'Upper Bounds'), cv2.getTrackbarPos('UpperV', 'Upper Bounds')])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('Result', res)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        save_color_presets(current_color, lower_bound, upper_bound)
    elif key in [ord('g'), ord('r'), ord('o'), ord('w')]:  # Preset selection keys
        preset_keys = {'g': 'green', 'r': 'red', 'o': 'orange', 'w': 'white'}
        current_color = preset_keys[chr(key)]
        for k in colors[current_color]:
            window = 'Lower Bounds' if 'Lower' in k else 'Upper Bounds'
            cv2.setTrackbarPos(k, window, colors[current_color][k])

cap.release()
cv2.destroyAllWindows()

import cv2

def initialize_camera(index=0):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print("Could not open video device")
        return None
    return cap

def capture_image(cap, filename="captured_image.jpg"):
    if cap is None:
        return

    ret, frame = cap.read()
    if ret:
        file_path = "images/capturedImage/" + filename
        cv2.imwrite(file_path, frame)
        print(f"Image saved as {file_path}")
    else:
        print("Failed to capture image")

def close_camera(cap):
    cap.release()
    cv2.destroyAllWindows()

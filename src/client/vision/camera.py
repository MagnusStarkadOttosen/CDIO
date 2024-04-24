import cv2

def capture_image(filename = "captured_image.jpg"):
    # Start the video capture object
    cap = cv2.VideoCapture(2)
    
    if not cap.isOpened():
        print("Could not open video device")
        return

    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret:
        file_path = "images/capturedImage/" + filename
        # Save the captured image to a file
        cv2.imwrite(file_path, frame)
        print(f"Image saved as {file_path}")
    else:
        print("Failed to capture image")

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

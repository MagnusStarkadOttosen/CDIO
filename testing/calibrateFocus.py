import cv2

def nothing(x):
    pass

def main():
    # Open the first connected camera
    cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open video device.")
        return

    # Get the property ID for manual focus
    # It might be different depending on your setup. Often it is 28.
    focus_property_id = 28  # You might need to adjust this value

    # Set camera to manual focus mode by setting autofocus off if possible
    # This might not work for all cameras as it depends on the driver support
    cap.set(focus_property_id, 0)  # This sets the camera to manual focus mode

    # Create a window
    cv2.namedWindow('Focus Calibration')

    # Create trackbar for changing the focus
    # The range of focus values can be very dependent on the camera
    # Typically, it might be from 0 to 100 or 0 to 255
    cv2.createTrackbar('Manual Focus', 'Focus Calibration', 0, 100, nothing)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Get current position of the focus slider
        focus_value = cv2.getTrackbarPos('Manual Focus', 'Focus Calibration')

        # Set the focus value
        cap.set(focus_property_id, focus_value)

        # Display the resulting frame
        cv2.imshow('Focus Calibration', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

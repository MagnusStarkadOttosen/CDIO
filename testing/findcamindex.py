import cv2

def find_camera_index():
    index = 0
    max_test_index = 10  # Set a reasonable limit to prevent endless loops

    while index <= max_test_index:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            print(f"No camera found at index {index}.")
        else:
            # Try to get at least one frame to confirm it's the correct camera
            ret, frame = cap.read()
            if ret:
                # Display the frame to visually confirm the correct camera
                cv2.imshow('Test Frame', frame)
                cv2.waitKey(1000)  # Display for 1 second
                cv2.destroyAllWindows()

                # Ask the user if this is the correct camera
                response = input(f"Is this the correct camera (index {index})? (y/n): ")
                if response.lower() == 'y':
                    cap.release()
                    return index
                else:
                    cap.release()
            else:
                print(f"Camera at index {index} is not returning images.")
                cap.release()
        index += 1

    return -1  # Return -1 if no correct camera is found

# Example usage
camera_index = find_camera_index()
if camera_index != -1:
    print(f"Using camera index: {camera_index}")
else:
    print("No suitable camera was found.")

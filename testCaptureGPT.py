import cv2

# Open the default camera (0 represents the default camera, you can change it if needed)
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Read frames from the camera stream
while True:
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the streaming frame (optional)
    cv2.imshow("Camera Stream", frame)

    # Capture only one frame and save it to an image file
    cv2.imwrite("captured_image.jpg", frame)
    print("Image captured successfully!")
    
    # Break out of the loop after capturing one frame
    break

# Release the camera
cap.release()

# Close any OpenCV windows
cv2.destroyAllWindows()

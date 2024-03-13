import cv2

# Open the video capture object using the device address
cap = cv2.VideoCapture('/dev/video4')

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Unable to open camera")
    exit()

# Read and display frames from the camera
while True:
    ret, frame = cap.read()

    # Check if the frame is valid
    if not ret:
        print("Error: Unable to read frame")
        break

    # Display the frame
    cv2.imshow('Frame', frame)

    # Check for the 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object and close all windows
cap.release()
cv2.destroyAllWindows()

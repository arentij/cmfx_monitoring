
import cv2, os
from matplotlib import pyplot as plt
# Create a VideoCapture object
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*"MJPG"))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2591)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1943)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1563)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Could not open camera")
    exit()

# Capture a frame from the camera
ret, frame = cap.read()



# plt.imshow(frame)
# print(frame)
cv2.imwrite('static/camphoto_temp.jpg', frame)
os.replace("static/camphoto_temp.jpg", "static/camphoto.jpg")

# Display the frame

# cv2.imshow('frame', frame)

# Release the camera
cap.release()

# Close all windows
# cv2.destroyAllWindows()
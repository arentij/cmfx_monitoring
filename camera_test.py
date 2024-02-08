
import cv2, os
from matplotlib import pyplot as plt
# Create a VideoCapture object
# cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap = cv2.VideoCapture("/dev/video0") # cam 2
# cap = cv2.VideoCapture("/dev/video4") # cam 1
# cap = cv2.VideoCapture("/dev/v4l/by-id/usb-Arducam_Arducam_5MP_Camera_Module_YL20230518V0-video-index0") # cam2
# cap = cv2.VideoCapture("/dev/v4l/by-id/usb-Arducam_Arducam_5MP_Camera_Module_YL20230518V0-video-index1") # cam2
# cap = cv2.VideoCapture("/dev/v4l/by-path/pci-0000:00:14.0-usb-0:1.1:1.0-video-index0")  # cam2
# cap = cv2.VideoCapture("/dev/v4l/by-path/pci-0000:00:14.0-usb-0:1.3:1.0-video-index0")  # cam1
# cap = cv2.VideoCapture("/dev/v4l/by-path/pci-0000:00:14.0-usb-0:2:1.0-video-index0")  # cam3
#                          "/dev/v4l/by-path/pci-0000:00:14.0-usb-0:2.3:1.0-video-index0"
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
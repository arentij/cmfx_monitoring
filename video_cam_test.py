import datetime
import subprocess
import cv2

# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
fps = 90
width = 640
height = 480

out = cv2.VideoWriter('static/mymovie_delayed90.avi', fourcc, fps, (width, height))

# Open the camera
camera_mount = "/dev/video6"
# command = "v4l2-ctl -d " + camera_mount + " -c exposure_time_absolute=3"
# subprocess.run(command, shell=True)

cap = cv2.VideoCapture(camera_mount, cv2.CAP_V4L2)  # Use '0' for the default camera, change if necessary
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FPS, fps)
# cap.set(cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Record for 10 seconds
record_duration = 10  # seconds
start_time = cv2.getTickCount()


time_started = datetime.datetime.now()
reading_times = []
writing_times = []
display_times = []
frame_to_frame_times = []

frames = []
start_time2 = cv2.getTickCount() / cv2.getTickFrequency()
n_frames = 0
while True:
    # print(n_frames)
    time_attempted_to_reach_frame = datetime.datetime.now()
    ret, frame = cap.read()
    time_after_read = datetime.datetime.now()
    reading_times.append((time_after_read-time_attempted_to_reach_frame).total_seconds()*1000)
    n_frames += 1
    if not ret:
        print("Error: Cannot read frame.")
        break

    # Write the frame
    frames.append(frame)
    # out.write(frame)
    time_to_write = datetime.datetime.now()
    writing_times.append((time_to_write-time_after_read).total_seconds()*1000)
    # Display the frame
    # cv2.imshow('frame', frame)

    time_to_show = datetime.datetime.now()
    display_times.append((time_to_show-time_to_write).total_seconds()*1000)
    # Check for 10 seconds recording limit
    current_time = cv2.getTickCount()
    current_time2 = cv2.getTickCount() / cv2.getTickFrequency()
    # if (current_time - start_time) > record_duration:
    #     break
    if (current_time - start_time) / cv2.getTickFrequency() >= record_duration:
        break

    # Break the loop if 'q' key is pressed
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    frame_to_frame_times.append((datetime.datetime.now()-time_attempted_to_reach_frame).total_seconds()*1000)
# Release everything when recording is done
print('Reading')
print(reading_times)
# print('Writing')
# print(writing_times)
print('Framerate')
print(frame_to_frame_times)

print(sum(frame_to_frame_times[1:-1])/len(frame_to_frame_times[1:-1]))
print(len(frames))
# print(sum(display_times[1:-1])/len(display_times[1:-1]))

for frame in frames:
    # cv2.imshow('frame', frame)
    out.write(frame)

cap.release()
out.release()
cv2.destroyAllWindows()




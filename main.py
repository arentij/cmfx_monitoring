from flask import Flask, render_template, request, jsonify
import threading
import datetime
import time
import cv2, os
from matplotlib import pyplot as plt
from flask import request
import smtp_code

app = Flask(__name__, static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/")
def index():
    return render_template('index.html')


def run_web_app():
    app.run(host='0.0.0.0', port=80)


@app.route('/return_one')
def return_one():
    a = request.args.get("a1", 0, type=float)
    b = request.args.get("b1", 0, type=float)
    # print('return a + rand() and b = ' + str(b))
    now = datetime.datetime.now()
    ssm = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()

    return jsonify(time=now
                   )


@app.route('/video')
def video():
    return render_template('video.html')


@app.route('/record_cameras')
def record_cameras():
    N_exp = request.args.get("n", 0, type=float)
    discharging = request.args.get("dsc", 0, type=float)
    disc_duration = request.args.get("dt", 0, type=float)
    now = datetime.datetime.now()
    ssm = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()

    print(ssm)
    print(N_exp)

    camera_device  = "/dev/video10"
    camera_device2 = "/dev/video2"
    camera_device3 = "/dev/video0"
    camera_device4 = "/dev/video8"
    # camera_device5 = "/dev/video4"

    timestr = time.strftime("%Y%m%d-%H%M%S")
    if discharging == 1:
        save_fldr = "/cmfx/video/exp" + str(N_exp) + "_" + timestr
        os.mkdir(save_fldr)
    else:
        save_fldr = "/cmfx/video/test/exp" + str(N_exp) + "_" + timestr
        os.mkdir(save_fldr)

    duration = 10
    # start_time = datetime.datetime.now()
    # for writing_ind in range(30):
    #     output_file = save_fldr + "/NN_260fps" + str(writing_ind) + ".avi"
    #
    #     file_written = capture_and_save_video(camera_device, output_file, duration, resolution=(640, 360), fps=260)
    #     end_time = datetime.datetime.now()
    #     print("Time taken", end_time-start_time)
    #     if file_written:
    #         break
    #     else:
    #         continue
    output_file  = save_fldr + "/N1_260fps.avi"
    output_file2 = save_fldr + "/N2_260fps.avi"
    output_file3 = save_fldr + "/N3_260fps.avi"
    output_file4 = save_fldr + "/N4_260fps.avi"
    # output_file5 = save_fldr + "/N4_260fps.avi"

    # file_written = capture_and_save_video(camera_device, output_file, duration, resolution=(640, 360), fps=260)
    resolution260 = (640, 360)
    resolution90 = (640, 480)
    fps260 = 260
    fps90 = 90

    now = datetime.datetime.now()

    north_cam1_260worker = threading.Thread(target=capture_and_save_video,
                                          args=([camera_device, output_file, duration, resolution260, fps260, now]))

    center1_260_worker = threading.Thread(target=capture_and_save_video,
                                             args=([camera_device2, output_file2, duration, resolution260, fps260, now]))

    north_cam2_260_worker = threading.Thread(target=capture_and_save_video,
                                            args=([camera_device3, output_file3, duration, resolution260, fps260, now]))

    south_cam1_260_worker = threading.Thread(target=capture_and_save_video,
                                             args=([camera_device4, output_file4, duration, resolution260, fps260, now]))


    north_cam1_260worker.start()
    time.sleep(0.02)
    center1_260_worker.start()
    time.sleep(0.02)
    north_cam2_260_worker.start()
    time.sleep(0.02)
    south_cam1_260_worker.start()

    time.sleep(0.02)


    # north_cam120worker = threading.Thread(target=capture_and_save_video,
    #                                       args=([camera_device5, output_file2, duration, resolution90, fps90, now]))
    # north_cam120worker.start()

    return jsonify(time=now, n=N_exp, dsc=discharging, duration=disc_duration)


def capture_and_save_video(camera_device, output_file, duration, resolution, fps, created=datetime.datetime.now()):
    # record_video(filename='output.mp4', duration=10):
    # Define the video capture device
    # start_time = cv2.getTickCount()

    # time_started = datetime.datetime.now()

    reading_times = []
    writing_times = []
    display_times = []
    frame_to_frame_times = []

    frames = []
    for cam_reach_attempt in range(60):
        print(cam_reach_attempt)
        print(fps)
        camera_reached = True
        cap_north = cv2.VideoCapture(camera_device, cv2.CAP_V4L2)
        cap_north.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        # %%%%%%%
        # cap = cv2.VideoCapture(camera_mount, cv2.CAP_V4L2)  # Use '0' for the default camera, change if necessary
        # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        # %%%%%%%
        # Check if the camera is opened successfully
        if not cap_north.isOpened():
            print("Error: Could not open the camera" + camera_device)
            continue
        # else:
        #     time.sleep(0.005)

        cap_north.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        cap_north.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        cap_north.set(cv2.CAP_PROP_FPS, fps)
        # cap_north.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
        # cap_north.set(cv2.CAP_PROP_GAIN, 0)
        # cap_north.set(cv2.CAP_PROP_BRIGHTNESS, -64)
        # cap_north.set(cv2.CAP_PROP_EXPOSURE, 2047)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        # fourcc = cv2.VideoWriter_fourcc(*'MJPG')

        out = cv2.VideoWriter(output_file, fourcc, fps, resolution)

        # out = cv2.VideoWriter(output_file)
        # Record video for the specified duration
        start_time = cv2.getTickCount() / cv2.getTickFrequency()
        print(start_time)

        # new
        while True:
            time_attempted_to_reach_frame = datetime.datetime.now()
            ret, frame = cap_north.read()
            time_after_read = datetime.datetime.now()

            if not ret:
                print("Error: Cannot read frame.")
                camera_reached = False
                break

            # Write the frame
            frames.append(frame)
            reading_times.append((time_after_read - created).total_seconds() * 1000)
            # out.write(frame)

            # Display the frame
            # cv2.imshow('frame', frame)


            # Check for 10 seconds recording limit
            current_time = cv2.getTickCount() / cv2.getTickFrequency()
            if (current_time - start_time) > duration:
                # if (time_started - time_to_show).total_seconds() >= record_duration:
                # print("Time limit reached")
                # print()
                # print(cv2.getTickFrequency())
                break

            # Break the loop if 'q' key is pressed
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            # frame_to_frame_times.append(
            #     (datetime.datetime.now() - time_attempted_to_reach_frame).total_seconds() * 1000)

        if not camera_reached:
            continue
        # old
        # while True:
        #     ret, frame = cap_north.read()
        #     if not ret:
        #         print('camera returned none')
        #         successfull_read = False
        #         return False
        #     out.write(frame)
        #     current_time = cv2.getTickCount() / cv2.getTickFrequency()
        #     # print(current_time)
        #     if (current_time - start_time) > duration:
        #         break

        # Release the video capture and writer objects
        print('Now lets write the files')
        print(len(frames))
        for frame in frames:
            # cv2.imshow('frame', frame)
            out.write(frame)
        count = 0

        if True:
            fldr = output_file[0:-4]
            # print(output_file)
            # print(fldr)
            os.mkdir(fldr)
            for frame in frames:
                cv2.imwrite(fldr + "/frame%d.jpg" % count, frame)
                count += 1

        out.release()
        cap_north.release()
        # Close all OpenCV windows
        cv2.destroyAllWindows()
        # print(f"Video recording completed: {filename}")
        output_file2 = output_file[0:-4] + ".txt"
        # Open the file in write mode
        with open(output_file2, 'w') as file:
            # Iterate over each number in the list
            file.write(created.strftime('%H:%M:%S.%f') + '\n')
            for num in reading_times:
                # Write each number to the file
                file.write(str(num) + '\n')
        # with open('output_file2, 'w', newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writerows(a)

        return True
    return False


def read_camera():
    while True:
        # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap = cv2.VideoCapture("/dev/video4")  # this is the camera2
        # cap = cv2.VideoCapture("/dev/mycam1")
        # cap = cv2.VideoCapture("/dev/v4l/by-path/pci-0000:00:14.0-usb-0:1.1:1.0-video-index0")
        # cap = cv2.VideoCapture("/dev/v4l/by-path/pci-0000:00:14.0-usb-0:2:1.0-video-index0")  # cam3

        # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*"MJPG"))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2591)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1943)

        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        try:
            ret, frame = cap.read()
            cap.release()
        except:
            print('Camera 1 is unreachable')
        # print(ret)

        if ret:
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (50, 50)
            fontScale = 1
            color = (255, 0, 255)
            thickness = 2
            now = datetime.datetime.now()  # now.strftime("%m/%d/%Y, %H:%M:%S")
            frame_cropped = crop_img(frame, 0.52, 0.5, 0.32, 0.32)
            frame = cv2.putText(frame_cropped, 'Last updated ' + now.strftime("%m/%d/%Y, %H:%M:%S"), org, font,
                                fontScale, color, thickness, cv2.LINE_AA)
            # print(frame.shape[0])
            # print(frame.shape[1])
            cwd = "/home/pereval/PycharmProjects/cmfx_monitoring"

            cv2.imwrite(cwd + '/static/camphoto_temp2.jpg', frame)

            for attempt in range(10):
                try:
                    os.replace(cwd + "/static/camphoto_temp2.jpg", cwd + "/static/camphoto2.jpg")
                    # print('Written another image 2')
                    break
                except PermissionError:
                    time.sleep(0.1)
                    print('Got the permission error, not writing this file for now')
                except FileNotFoundError:
                    time.sleep(1)
                    print('Files do not exist')
        # cam2
        time.sleep(1)

        cap2 = cv2.VideoCapture("/dev/video6")  # this is cam1
        # cap2 = cv2.VideoCapture("/dev/v4l/by-path/pci-0000:00:14.0-usb-0:1.3:1.0-video-index0")
        # cap2 = cv2.VideoCapture("/dev/v4l/by-path/pci-0000:00:14.0-usb-0:2:1.0-video-index0")  # cam3

        # cap2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*"MJPG"))
        cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 2591)
        cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 1943)
        try:
            ret, frame = cap2.read()
            cap2.release()
            # print('read cam2')
        except:
            print('Camera 2 is unreachable')
        # print(ret)
        if ret:
            # print('ret - true')
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (50, 50)
            fontScale = 1
            color = (255, 0, 255)
            thickness = 2
            now = datetime.datetime.now()

            frame_cropped = crop_img(frame, 0.45, 0.5, 0.32, 0.32)
            frame = cv2.putText(frame_cropped, 'Last updated ' + now.strftime("%m/%d/%Y, %H:%M:%S"), org, font,
                                fontScale, color, thickness, cv2.LINE_AA)
            cwd = "/home/pereval/PycharmProjects/cmfx_monitoring"

            cv2.imwrite(cwd + '/static/camphoto_temp.jpg', frame)

            for attempt in range(10):
                try:
                    os.replace(cwd + "/static/camphoto_temp.jpg", cwd + "/static/camphoto.jpg")
                    # print('Written another image 1')
                    break
                except PermissionError:
                    time.sleep(0.1)
                    print('Got the permission error, not writing this file for now')

        # and now lets wait a bit
        time.sleep(3)

    return True


def crop_img(frame, mid_x, mid_y, size_x, size_y):
    height = frame.shape[0]
    width = frame.shape[1]
    # size_h = range(,
    # size_w = range(max(0, int(width * (mid_y - size_y / 2))), )
    cropped_frame = frame[max(0, int(height * (mid_x - size_x / 2))):min(height, int(height * (mid_x + size_x / 2))),
                    max(0, int(width * (mid_y - size_y / 2))):min(width, int(width * (mid_y + size_y / 2)))]

    return cropped_frame


def sending_emails():
    now = datetime.datetime.now()
    ssm = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    if ssm > 12 * 3600:
        sent_today = True
    else:
        sent_today = False

    while True:
        now = datetime.datetime.now()
        ssm = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        # print(ssm/3600)
        # print(sent_today)
        # if it is past midnight lets switch back to "havent sent today"
        if ssm < 3600:
            sent_today = False
        # if it is noon and we haven't sent today, lets send!
        elif ssm > 12 * 3600 and not sent_today:
            destination = ['artur_email', 'carlos_email', 'artur']
            # destination = ['artur_email']

            if smtp_code.sendmail(destination):
                print('I just sent the emails')
                sent_today = True
            else:
                print(now)
                print('Something went wrong with the emails')
                time.sleep(30)
                continue
        else:
            # otherwise lets sleep
            time.sleep(10)
    return True


if __name__ == "__main__":
    print('Started program')
    web_app_worker = threading.Thread(target=run_web_app, args=())
    web_app_worker.start()
    print('Web app started')

    camera_update_worker = threading.Thread(target=read_camera, args=())
    # camera_update_worker.start()
    print('Camera updater started')

    time.sleep(20)
    email_send_worker = threading.Thread(target=sending_emails, args=())
    email_send_worker.start()
    print('Emailer is working')

    # print(app.route())
    # sys.exit()

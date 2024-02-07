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


def read_camera():
    while True:
        # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap = cv2.VideoCapture("/dev/video2")
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
            now = datetime.datetime.now()
            frame_cropped = crop_img(frame, 0.52, 0.5, 0.32, 0.32)
            frame = cv2.putText(frame_cropped, 'Last updated ' + now.strftime("%m/%d/%Y, %H:%M:%S"), org, font,
                                fontScale, color, thickness, cv2.LINE_AA)
            # print(frame.shape[0])
            # print(frame.shape[1])
            cwd = "/home/pereval/PycharmProjects/pythonProject/cmfx_monitoring"
            
            cv2.imwrite(cwd + '/static/camphoto_temp2.jpg', frame)

            for attempt in range(10):
                try:
                    os.replace(cwd + "/static/camphoto_temp2.jpg", cwd + "/static/camphoto2.jpg")
                    # print('Written another image 2')
                    break
                except PermissionError:
                    time.sleep(0.1)
                    print('Got the permission error, not writing this file for now')

        # cam2
        time.sleep(1)

        cap2 = cv2.VideoCapture("/dev/video4")
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
            cwd = "/home/pereval/PycharmProjects/pythonProject/cmfx_monitoring"

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
            destination = ['artur_email', 'artur', 'carlos_email']

            smtp_code.sendmail(destination)
            print('I just sent the emails')
            sent_today = True
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
    camera_update_worker.start()
    print('Camera updater started')

    time.sleep(10)
    email_send_worker = threading.Thread(target=sending_emails, args=())
    email_send_worker.start()
    print('Emailer is working')

    # print(app.route())
    # sys.exit()

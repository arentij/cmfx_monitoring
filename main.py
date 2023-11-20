from flask import Flask, render_template, request, jsonify
import threading
import datetime
import time
import cv2, os
from matplotlib import pyplot as plt


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
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2591)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1943)

    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:

        try:
            ret, frame = cap.read()
        except:
            print('Camera is unreachable')

        if ret:
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (50, 50)
            fontScale = 2
            color = (255, 0, 255)
            thickness = 2
            now = datetime.datetime.now()
            frame = cv2.putText(frame, 'Last updated ' + now.strftime("%m/%d/%Y, %H:%M:%S"), org, font,
                                fontScale, color, thickness, cv2.LINE_AA)

            cv2.imwrite('static/camphoto_temp.jpg', frame)

            for attempt in range(10):
                try:
                    os.replace("static/camphoto_temp.jpg", "static/camphoto.jpg")
                    # print('Written another image')
                    break
                except PermissionError:
                    time.sleep(0.1)
                    print('Got the permission error, not writing this file for now')

        time.sleep(3)

    return True


if __name__ == "__main__":
    print('Started program')
    web_app_worker = threading.Thread(target=run_web_app, args=())
    web_app_worker.start()
    print('Web app started')

    camera_update_worker = threading.Thread(target=read_camera, args=())
    camera_update_worker.start()
    print('Camera updater started')



    # sys.exit()
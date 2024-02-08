import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import netifaces as ni
import numpy as np
from PIL import Image, ImageStat
import shutil
import time


def brightness(im_file):
    im = Image.open(im_file).convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]


def sendmail(destination=['artur_email']):

    team_list = dict(artur='8304994663@tmomail.net',
                artur_email='arentij@gmail.com',
                carlos='9257848145@msg.fi.google.com',
                carlos_email='romero@umbc.edu',
                )

    team = []
    for member in destination:
        try:
            team.append(team_list[member])
        except KeyError:
            print('Unknown destination ' + str(member))
    try:
        f1_name = "/home/pereval/PycharmProjects/cmfx_monitoring/static/camphoto.jpg"
        f2_name = "/home/pereval/PycharmProjects/cmfx_monitoring/static/camphoto2.jpg"
        with open(f1_name, 'rb') as f:
            img_data = f.read()
            greyscale_img = Image.open(f).convert('L')
            stat = ImageStat.Stat(greyscale_img)
            brght1 = stat.mean[0]
            # print(brght1)
            if brght1 < 50:
                print('The image is too dark')
                return False

        with open(f2_name, 'rb') as f:
            img_data2 = f.read()
            greyscale_img2 = Image.open(f).convert('L')
            stat2 = ImageStat.Stat(greyscale_img2)
            brght2 = stat2.mean[0]
            if brght2 < 50:
                print('The image 2 is too dark')
                return False

    except FileNotFoundError:
        return False

    msg = MIMEMultipart()
    msg['Subject'] = 'CMFX Pressure'
    msg['From'] = 'CMFX.monitor@gmail.com'
    msg['To'] = ', '.join(team)

    # ip = ni.ifaddresses('wlo1')[ni.AF_INET][0]['addr']

    text = MIMEText('cmfx.ireap.umd.edu')
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(
        f1_name))
    msg.attach(image)

    image2 = MIMEImage(img_data2, name=os.path.basename(
        f2_name))
    msg.attach(image2)

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    # s.starttls()
    # s.ehlo()
    s.login("CMFX.monitor@gmail.com", "rsjncajkwmsiodln")
    s.sendmail('CMFX Monitoring', team, msg.as_string())
    s.close()

    # now = datetime.datetime.now()  # now.strftime("%m/%d/%Y, %H:%M:%S")
    timestr = time.strftime("%Y%m%d-%H%M%S")

    f1_log_name = "/home/pereval/PycharmProjects/cmfx_monitoring/img_logs/C1" + timestr + ".jpg"
    f2_log_name = "/home/pereval/PycharmProjects/cmfx_monitoring/img_logs/C2" + timestr + ".jpg"
    shutil.copyfile(f1_name, f1_log_name)
    shutil.copyfile(f2_name, f2_log_name)

    return True


if __name__ == "__main__":
    destination = ['artur_email']
    print(sendmail(destination))



